#include <pybind11/pybind11.h>
#include "algo.h"

namespace py = pybind11;
PYBIND11_MODULE({module_name}, m) {{
    m.doc() = R"pbdoc(
        pybind11_cmake example
        -----------------------
        .. currentmodule:: {project_name}
        .. autosummary::
           :toctree: _generate
           add
    )pbdoc";

    m.def("add", &add, R"pbdoc(Add two numbers)pbdoc");

    py::class_<Calc>(m, "Calc")
    .def(py::init<double>(), py::arg("version"))
    .def("subtract", &Calc::subtract, py::arg("a"), py::arg("b"));
}}