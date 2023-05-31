# dna-storage

This repository contains the code for my Master's project on encoding schemes for archival DNA data storage.

**Title: *Decreasing error-rates in archival DNA data storage through constraint-driven encoding.***

**Research Question:** Can an FSM-based constraint-driven encoding scheme as presented by [Sella *et al.*](https://dl.acm.org/doi/abs/10.1145/3465332.3470880) be leveraged to mitigate errors which arise in the archival DNA data storage life-cycle?

### Setup Instructions

The following setup instructions should work for Linux and Mac systems. If using Windows, you may need to use a virtual machine or a terminal emulator such as [Cygwin](https://www.cygwin.com/). Python 3, pip, Rust and git will need to be installed. You can install Rust using [rustup](https://rustup.rs/).

Clone the repository and change directory into the root of the project.
```
git clone https://github.com/IzerOnadim/dna-storage.git
cd dna-storage
```
OR if using SSH:
```
git clone git@github.com:IzerOnadim/dna-storage.git
cd dna-storage
```
Once here, it is recommended to use a Python virtual environment for installing the required dependencies. You can create and activate a Python venv with the following:
```
python3 -m venv .venv
source .venv/bin/activate
```
If venv creation fails you may need to install [python3-venv](https://docs.python.org/3/library/venv.html), or simply proceed without a virtual environment.

You will need to install the dependancies. This can be done using pip (you will need [pip](https://pypi.org/project/pip/) if you don't already have it) with the following command:
```
pip install -r requirements.txt
```
Once the dependancies are successfully installed, you will need to add the compiled Rust libraries to your python environment. This can be done by changing directories into each of the rust projects and running the `maturin develop` command in release mode, like so:
```
cd rust/encoding
maturin develop --release
cd ../viterbi
maturin develop --release
```
If this fails it may be because Rust's package manager `cargo` is not in your PATH. Install Rust from [rustup](https://rustup.rs/) and make sure `cargo` is in your PATH. Upon successfully compiling and installing the Rust libraries, the project is ready to run. Change directory back to the root of the project. As a test you can run the examples.py file. The output of this is not important, but it should complete without errors if all prior steps were completed successfully.
```
python3 examples.py
```
If you chose to use a virtual environment to install your dependancies, you can deactivate it with the following:
```
deactivate
```
After which point the code will no longer work.
