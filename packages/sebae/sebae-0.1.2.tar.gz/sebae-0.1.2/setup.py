from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        packages=find_packages("src"),  # include all packages under src
        package_dir={"": "src"},   # tell distutils packages are under src
        include_package_data=True
    )