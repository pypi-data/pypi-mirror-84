import setuptools as s
f=open("readme.txt","r")
ld=f.read()
f.close()
s.setup(
    name = "PyQE_Solver",
    version="4.0.0",
    author = "Piyush",
    author_email="pyushsomani97@gmail.com",
    description="Quadratic Equation Solver",
    url="https://github.com/PS218909/ROOT",
    long_description=ld,
    long_description_content_type='text/markdown',
    packages=s.find_packages(),
    python_requires=">=3.6"
    )

                
