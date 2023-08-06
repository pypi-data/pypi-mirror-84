cmake_minimum_required(VERSION 2.8.12)
project({project_name})

add_executable(debug src/main.cc)
target_include_directories(debug PUBLIC include)


add_subdirectory(3rd/pybind11)
include_directories(include PUBLIC)
pybind11_add_module({module_name} src/binding.cc)
target_compile_features({module_name} PUBLIC cxx_std_14)