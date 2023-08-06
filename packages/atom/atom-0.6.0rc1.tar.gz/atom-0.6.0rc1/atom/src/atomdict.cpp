/*-----------------------------------------------------------------------------
| Copyright (c) 2014-2019, Nucleic
|
| Distributed under the terms of the BSD 3-Clause License.
|
| The full license is in the file LICENSE, distributed with this software.
|----------------------------------------------------------------------------*/
#include <cppy/cppy.h>
#include "atomdict.h"
#include "packagenaming.h"

namespace atom
{

namespace
{

inline bool should_validate( AtomDict* dict )
{
	return dict->pointer->data() && ( pyobject_cast( dict->m_key_validator ) != Py_None ||
                                      pyobject_cast( dict->m_value_validator ) != Py_None );
}


PyObject* validate_key( AtomDict* dict, PyObject* key )
{
    CAtom* atom = dict->pointer->data();
    Member* key_val = dict->m_key_validator;

    cppy::ptr key_item( cppy::incref( key ) );
    if( key_val && atom )
    {
        key_item = key_val->full_validate( atom, Py_None, key_item.get() );
        if( !key_item )
            return 0;
    }
    return key_item.release();

}

PyObject* validate_value( AtomDict* dict, PyObject* value )
{
    CAtom* atom = dict->pointer->data();
    Member* value_val = dict->m_value_validator;

    cppy::ptr value_item( cppy::incref( value ) );
    if( value_val && atom )
    {
        value_item = value_val->full_validate( atom, Py_None, value_item.get() );
        if( !value_item )
            return 0;
    }
    return value_item.release();

}


int merge_items( PyObject* dict, PyObject* item, PyObject* kwargs )
{
	int ok = 0;
	if( item )
	{
		if( PyObject_HasAttrString( item, "keys" ) )
		{
			ok = PyDict_Merge( dict, item, 1 );
		}
		else
		{
			ok = PyDict_MergeFromSeq2( dict, item, 1 );
		}
	}
	if( ok == 0 && kwargs )
	{
		ok = PyDict_Merge( dict, kwargs, 1 );
	}
	return ok;
}


PyObject* AtomDict_new( PyTypeObject* type, PyObject* args, PyObject* kwargs )
{
	cppy::ptr self( PyDict_Type.tp_new( type, args, kwargs ) );
	if( !self )
	{
		return 0;
	}
    atomdict_cast( self.get() )->pointer = new CAtomPointer();
    return self.release();
}


int AtomDict_clear( AtomDict* self )
{
	Py_CLEAR( self->m_key_validator );
	Py_CLEAR( self->m_value_validator );
	return PyDict_Type.tp_clear( pyobject_cast( self ) );
}


int AtomDict_traverse( AtomDict* self, visitproc visit, void* arg )
{
	Py_VISIT( self->m_key_validator );
	Py_VISIT( self->m_value_validator );
#if PY_VERSION_HEX >= 0x03090000
    // This was not needed before Python 3.9 (Python issue 35810 and 40217)
    Py_VISIT(Py_TYPE(self));
#endif
    // PyDict_type is not heap allocated so it does visit the type
	return PyDict_Type.tp_traverse( pyobject_cast( self ), visit, arg );
}


void AtomDict_dealloc( AtomDict* self )
{
	cppy::clear( &self->m_key_validator );
	cppy::clear( &self->m_value_validator );
	PyDict_Type.tp_dealloc( pyobject_cast( self ) );
}


int AtomDict_ass_subscript( AtomDict* self, PyObject* key, PyObject* value )
{
    cppy::ptr key_ptr( cppy::incref( key ) );
    cppy::ptr value_ptr( cppy::xincref( value ) );
	if( value && should_validate( self ) )
	{
        key_ptr = validate_key( self, key_ptr.get() );
		if( !key_ptr )
		{
			return -1;
		}

        value_ptr = validate_value( self, value_ptr.get() );
		if( !value_ptr )
		{
			return -1;
		}
	}
	return PyDict_Type.tp_as_mapping->mp_ass_subscript( pyobject_cast( self ), key_ptr.get(), value_ptr.get() );
}


PyObject* AtomDict_setdefault( AtomDict* self, PyObject* args )
{
	PyObject* key;
	PyObject* dfv = Py_None;
	if( !PyArg_UnpackTuple( args, "setdefault", 1, 2, &key, &dfv ) )
	{
		return 0;
	}
	PyObject* value = PyDict_GetItem( pyobject_cast( self ), key );
	if( value )
	{
		return cppy::incref( value );
	}
	if( AtomDict_ass_subscript( self, key, dfv ) < 0 )
	{
		return 0;
	}
	return cppy::incref( dfv );
}


PyObject* AtomDict_update( AtomDict* dict, PyObject* args, PyObject* kwargs )
{
    PyObject* item = 0;
	if( !PyArg_UnpackTuple( args, "update", 0, 1, &item ) )
	{
		return 0;
	}

	if( !should_validate( dict ) )
	{
		if( merge_items( pyobject_cast( dict ), item, kwargs ) < 0 )
        {
            return 0;
        }
        else
        {
            return cppy::incref( Py_None );
        }
	}

	cppy::ptr temp( PyDict_New() );
	if( !temp )
	{
		return 0;
	}
	if( merge_items( temp.get(), item, kwargs ) < 0 )
	{
		return 0;
	}

    if( AtomDict::Update( dict, temp.get() ) < 0 )
	{
		return 0;
	}

	return cppy::incref( Py_None );
}


static PyMethodDef AtomDict_methods[] = {
	{ "setdefault",
		( PyCFunction )AtomDict_setdefault,
		METH_VARARGS,
		"D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D" },
	{ "update",
		( PyCFunction )AtomDict_update,
		METH_VARARGS | METH_KEYWORDS,
		"D.update([E, ]**F) -> None. Update D from dict/iterable E and F" },
	{ 0 } // sentinel
};


static PyType_Slot AtomDict_Type_slots[] = {
    { Py_tp_dealloc, void_cast( AtomDict_dealloc ) },              /* tp_dealloc */
    { Py_mp_ass_subscript, void_cast( AtomDict_ass_subscript ) },  /* mp_ass_subscript */
    { Py_tp_traverse, void_cast( AtomDict_traverse ) },            /* tp_traverse */
    { Py_tp_clear, void_cast( AtomDict_clear ) },                  /* tp_clear */
    { Py_tp_methods, void_cast( AtomDict_methods ) },              /* tp_methods */
    { Py_tp_base, void_cast( &PyDict_Type ) },                     /* tp_base */
    { Py_tp_new, void_cast( AtomDict_new ) },                      /* tp_new */
    { 0, 0 },
};


} // namespace


// Initialize static variables (otherwise the compiler eliminates them)
PyTypeObject* AtomDict::TypeObject = NULL;


PyType_Spec AtomDict::TypeObject_Spec = {
	PACKAGE_TYPENAME( "atomdict" ),             /* tp_name */
	sizeof( AtomDict ),                         /* tp_basicsize */
	0,                                          /* tp_itemsize */
	Py_TPFLAGS_DEFAULT
	| Py_TPFLAGS_BASETYPE
	| Py_TPFLAGS_HAVE_GC
	| Py_TPFLAGS_HAVE_VERSION_TAG,              /* tp_flags */
    AtomDict_Type_slots                         /* slots */
};


PyObject* AtomDict::New( CAtom* atom, Member* key_validator, Member* value_validator )
{
    cppy::ptr self( PyDict_Type.tp_new( AtomDict::TypeObject, 0, 0 ) );
	if( !self )
	{
		return 0;
	}
    cppy::xincref( pyobject_cast( key_validator ) );
    atomdict_cast( self.get() )->m_key_validator = key_validator;
    cppy::xincref( pyobject_cast( value_validator ) );
    atomdict_cast( self.get() )->m_value_validator = value_validator;
    atomdict_cast( self.get() )->pointer = new CAtomPointer( atom );
    return self.release();
}


int AtomDict::Update( AtomDict* dict, PyObject* value )
{
	cppy::ptr validated_dict( PyDict_New() );
	PyObject* key;
	PyObject* val;
	Py_ssize_t index = 0;
	while( PyDict_Next( value, &index, &key, &val ) )
	{
        cppy::ptr key_ptr( cppy::incref( key ) );
        key_ptr = validate_key( dict, key_ptr.get() );
		if( !key_ptr )
		{
			return -1;
		}

        cppy::ptr val_ptr( cppy::incref( val ) );
        val_ptr = validate_value( dict, val_ptr.get() );
		if( !val_ptr )
		{
			return -1;
		}

        if( PyDict_SetItem( validated_dict.get(), key_ptr.get(), val_ptr.get() ) != 0 )
        {
            return -1;
        }

	}

	if( PyDict_Update( pyobject_cast( dict ), validated_dict.get() ) < 0 )
	{
		return -1;
	}

    return 0;
}


bool AtomDict::Ready()
{
    // The reference will be handled by the module to which we will add the type
	TypeObject = pytype_cast( PyType_FromSpec( &TypeObject_Spec ) );
    if( !TypeObject )
    {
        return false;
    }
    return true;
}


} // namespace atom
