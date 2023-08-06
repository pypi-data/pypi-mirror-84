#include <Python.h>
#include <stdio.h>

void fly(const char *name)
{
    printf("%s is flying.\n", name);
}

static PyObject *bird_fly(PyObject *self, PyObject *args)
{
    const char *name;
    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
    fly(name);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef bird_methods[] = {
    { "fly", bird_fly, METH_VARARGS, "Bird fly" },
{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initbird_c(void)
{
    //PyImport_AddModule("bird");
    Py_InitModule("bird_c", bird_methods);
}
