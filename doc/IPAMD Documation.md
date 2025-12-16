# IPAMD Documentation
*v0.0.10*\
Author: Xiaoyang Liu
---

## Contents
- [Introduction](#Introduction)
- [Installation](#Installation)
- [Usage](#Usage)
- [Second-time-development](#Second-time-development)
- [Supporting](#Supporting)

## Introduction
IPAMD is a plugin-based Python package designed to simulate biomolecules using CG methods. It provides a simple and efficient way to build, simulate, and analyze biomolecular systems. Currently, IPAMD supports several one bead one amino acid CG models, such as the HPS model, the Mpipi model. More CG models will be added in the future. IPAMD is designed to be easy to use and extend. The user can easily add new functions to this package by writing a plugin. The detailed instruction on writing a plugin is shown in the [second-time-development](#Second-time-development) section.

## Installation
### prerequisites
IPAMD is a Python package. To use this package, you need to have Python installed on your system. You can download Python from the official website. But installing Python by Miniforge is recommended. Miniforge can be downloaded by the link below.
[conda-forge/miniforge: A conda-forge distribution.](https://github.com/conda-forge/miniforge)
This package *MUST* run in python 3.12. You can create a virtual environment by mamba.
```bash
mamba create -n ipamd python==3.12
mamba activate ipamd
```

### Install from source code
To install this package from the source code, you need firstly to change your working directory to the root directory of the package, and then run the following command.
```bash
python setup.py install
#or
pip install .  #recommended
```

### Install from Pypi
Currently, this package is also available on PyPI. You can also install it by pip. By this way, you can get the latest stable version of this package.
```
pip install ipamd
```

## Usage
Import ipamd in your python script, and then you can use the functions provided by this package. You can find the detailed usage of each function in the following sections. Example code is also available in the demo folder.

### Data storage
By default, the output data is managed by ipamd in another directory to make your working space clean. The data directory is located at `~/ipamd_output`. If you don't like this behavior, you can change this by modifying the config file located at `/etc/ipamd/config.json`. The detailed instruction on modifying the config file is shown in the [configuration](#configuration) section.

### App
App is the main module of this package. The first thing you need to do is to import App class from this package and create an instance. When creating an instance of App, you can set the name of the project. The name of the project will be used as the name of the output directory. If the name is not set, the default name will be a random string.
```python
from ipamd import App

app = App(name='protein')
```
After creating an app object, all the plugins will be loaded automatically by default. You can then use the functions provided by this package.

We also provide several functions in the App class to help you init your simulation. The functions are listed below.

- `__init__`: initialize the app object. There are three parameters in this function.
- `name`: the name of the project. Default is a random string.

- `init_working_dir`: whether to initialize the working directory. Default is True. In normal cases, you should not change this parameter.

- `gpu_id`: the id of the GPU to use. Default is 0. The id is the same with the value shown by `nvidia-smi`.

- `gen_link`: this function can generate a symbolic link to the data directory. This function is useful when you want to use the data files provided by this package.\

- `available_ff`: print the available force fields in your system.

- `load_file`: copy a data file from current working directory to the data directory of this package. If you choose not to manage the data files by this package, you can ignore this function. If you set `$decentralized` in your config file, this function shouldn't be used.
- `export_file`: copy a data file from the data directory of this package to the current working directory. If you choose not to manage the data files by this package, you can ignore this function. The first parameter is the name of the file to export, and the second parameter is the target directory. If the target directory is not set, the file will be copied to the current working directory.

### Models
Some common concepts in MD simulation and other things are defined in `ipamd.public.models.*`. In most times you don't need to create these objects manually, as the functions provided by this package will create these objects for you. So there would just be a brief of these models.
#### Atom
The Atom object defines the velocity, the charge and the mass of an atom. If these values are set, they will override the default values defined in the force field.

#### Molecule
Molecule object defines the position of all atoms and the bonding relationship between atoms.

#### Frame
Frame is the object containing several molecules. There are two ways of reading the molecule data contained in a frame. The first way is to directly read the molecule array of a frame object. The second way is to run `frame.properties()`. The returned value is a Dist containing the properties of the system.

#### Environment
The Environment object defines the simulation environment, such as the temperature, the dielectric constant et al.
You can create an environment object by
```python
from ipamd.public.models.md import Environment
env = Environment()
```
You can also provide a parameter of environment to the initial statement. Then the environment object will be created from the corresponding template. Currently available names include `'pure water'` and `'normal saline'`.

#### Box
Box object defines the simulation box. The box contains several frames and the environment. If you want to read the data in a specific frame, you should first run `box.frame(n)` to set the active frame and then run `box.c`

#### Unit
The default length and time unit in IPAMD is nanometer, picosecond. If you want to use other units, you can use the Unit class to convert the units. There is an example of using angstrom and femtosecond in IPAMD.
```python
from ipamd.public.models.md import Unit
time = 100 * Unit.TimeScale.fs  
length = 100 * Unit.LengthScale.A
```

#### Sequence
The DNA, RNA and protein sequence are represented by similar way. You can create a sequence object by the functions provided by sakuanna module. The sequence object was written in a List-like way. You can modify, slice and iterate the sequence object like a list.

### running a simulation
You need to create a simulation box first, and then create a simulation object by `simulation = app.simulation.new_simulation(parameters)`. Finally, you can run the simulation by `simulation.run(timesteps)`. The parameters available when creating a simulation object are listed below.
- `simulation_box`: the simulation box object.
- `job_name`: the name of the job. Default is `simulation`. All the output files will have this prefix.
- `dt`: the time step of the simulation. Default is 0.01 ps.
- `total_time`: the total time of the simulation. Default is 0, which means no simulation will be run.
- `snap_shot`: the interval of writing the snapshot file. Default is 0, which means no snapshot file will be written.
- `run_step`: the number of steps to run. Default is 0, which means no simulation will be run. 
- `period`: the interval of writing the trajectory. If the `total_time` and `snap_shot` is set, the `run_step` and `period` will be discarded.
- `thermo_bath`: the integrator to use. Default is `langevin_nvt`.
- `res_auto_read`: whether to read the restart file automatically. Default is True. This will be helpful if you want to do some analysis after the simulation.
- `minimize_energy`: whether to minimize the energy before running the simulation. Default is True.

### configuration converter
IPAMD also provides some tools for configuration conversion. You can call these tools by executing `box.converter_function()`. These tools include:

`align_center`: align the mass center of the whole system to the center of the box. No parameter is needed in this function.

`merge_nearst`: sometimes molecules in a droplet would be seperated by the simulation box. This function can merge these molecules. No parameter is needed in this function.

`read_xml`: read the configuration from a .xml file. The only required parameter is `filename`, which is the name of the .xml file. Note that the filename you provided shouldn't have a .xml extension.

`unwrap`: in MD simulation, a pbc (periodic boundary condition) is usually used. All the particles out of the box will be wrapped back to the box. This function can unwrap the particles to their original position. No parameter is needed in this function. This function is useful when you analyze the diffusion of the proteins.

`to_aa`: this function converts cg protein to all-atom protein. The only parameter is the output filename of the all-atom protein.
*Note:* This function uses cg2all as its computing backend, so you must ensure that cg2all is installed on your computer and can be called in the terminal.

`to_cif`: save the configuration to a .cif file. The only required parameter is `filename`, which is the name of the .cif file.

`to_pdb`: similar to `to_cif`, but save the configuration to a .pdb file.

`to_xml`: similar to `read_xml`, but save the configuration to a .xml file. XML format is the native format of IPAMD, so you can use this function to save your simulation box and continue your simulation later.
### force fields
All the force fields in IPAMD are provided in .xml format. The force field files are located in the data directory of this package. Each force field file contains two parts, the first part is the atom definition and the second part is the interaction potentials. The atom definition part contains the charge and the mass of each CG bead. The interaction potential part contains the interaction form and the parameters of each interaction potential. The format of the force field file is shown below.
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<ff>
    <atom_definition>
        <ATOM charge="0" mass="0"/>
    </atom_definition>
    <ff_param>
        <FORCE_NAME global_parameter="value">
            <ATOM parameter="value"/>
        </FORCE_NAME>
    </ff_param>
</ff>
```
You can also define parameters that varying with the simulation condition by setting the value with a string starting with `compute:`. After the prefix, you can write a python expression to compute the value. The runtime values in environment can be used by `{physical_value}`.

During the runtime, you can also create a dict with the same format as the force field file, and load it to the app by `app.use(dict)`.

### modules
The main functions of this package are organized in several modules of app object. The modules and the contained functions are listed as bellow.

#### builder
The builder module contains some functions for building the system. Detailed information of each function is listed as bellow.

`app.builder.af2`: this function can call the alphafold2(colabfold) installed on your computer to generate the initial structure of the protein. After running this function, a pdb file of the protein will be written in the working directory. An instruction on installing colabfold is available on [YoshitakaMo/localcolabfold: ColabFold on your local PC](https://github.com/YoshitakaMo/localcolabfold). The only required parameters of this function is `protein_sequence`. This parameter is a protein sequence object.

example:
```python
app.builder.af2('ELN', 'VPGAGVPGAGVPGAG')
```
*Note:* You should make sure that colabfold_batch command is available in your system.

`app.builder.box_from_xml`: this function can generate a simulation box from a .xml file. The only required parameter of this function is `filename`, which is the name of the .xml file. This function is useful when you want to build a complex system with multiple molecules or continue your simulation from a previous simulation. 

`app.builder.cg_molecule_from_pdb`: this function can generate a coarse-grained molecule from a pdb file. The name of the CG beads will be the same as the residue name in the pdb file. The required parameters of this function is `file_name`, which is the name of the pdb file. The other optional parameters include `rigid_range`, this parameter indicates which residues should be regarded as rigid body. The value of this parameter should like `'5-20,30-50'`, which means residues from 5 to 20 and from 30 to 50 are rigid body. Default is None, which means all residues are flexible.

`download_pdb`: this function can download a pdb file from RCSB PDB database. The only required parameter of this function is `id`, which is the id of in RCSB PDB database. The pdb file will be written in the working directory.

`app.builder.gen_elastic_network`: this function can generate an elastic network for a protein. The two parameters of this function are `molecule`, which is the target molecule, and `max_gap`, which is the maximum distance between two residues from two different structural regions. Default value of `max_gap` is 4. This function will return two values, the first one is the target molecule, and the second one is the extra force field generated by this function. You need to use this extra force field in your simulation to make the elastic network work.

Example:
```python
mol, extra_ff = app.builder.gen_elastic_network(
    molecule,
    max_gap=4
)
app.use(extra_ff)
```

`app.builder.linear_protein`: this function can generate a linear protein with a specific sequence. The required parameters of this function are `protein`, which is a protein sequence object.

`app.builder.protein_from_pdb`
This function can automatically generate the protein object from a pdb file. The pdb file should be located in the working directory. The parameters of this function include
- `file_name`: the name of the pdb file.
- `ignoring_h`, whether to ignore the hydrogen atoms in the pdb file. Default is True.
- `cg`: Where should the coarse-grained bead locate. Available values are `alpha` and `mass_center`. Default is `mass_center`.
- `rigid_range`, this parameter indicates which residues should be regarded as rigid body. Reference `cg_molecule_from_pdb` for this parameter.
- `rigid_from_plddt`, determine whether a residue is rigid body by plddt score from alphafold2. Default is `False`.
- `threshold`, when `rigid_from_plddt` is set true, this parameter determines when plddt score is larger than the threshold, the residue can be regarded as rigid body, i.e., protein with structure. Default is 70.
- `max_gap`, reference `gen_elastic_network` for this parameter.

`app.builder.spiral_protein`: this function can generate a protein with the shape of Archimedean spiral. The required parameters of this function is the same with `linear_protein`. Another optional parameter is `d`. This value indicates the radial distance. The default value is 0.38 nm.

example:
```python
protein = app.builder.protein_from_pdb(
    'protein',
    rigid_from_plddt=True
)
```

#### genbox
This part contains some functions for placing molecules in the simulation box. The basic usage is to run `box.gen_function(parameters)`. Available functions are listed below.

`place_molecule_randomly`: randomly place molecules in the simulation box. The required parameters of this function are listed bellow.
- `molecule`, the molecule object to add; n, the number of molecules.
- `threshold`, the minimum distance between two particles, default is 1.
- `max_tries`, maximum times the function will try to place a molecule, default is 5.
- `strict`, if this parameter is set to true, the program will continue trying until the  target `n` is reached, default is false.
- `allow_out_of_box`, if the molecules are allowed to be placed over the box boundary, default is true. If you want to generate box by `sub_box`, this option will be useful.

`place_molecule_periodically`: periodically place molecules in the simulation box. The required parameters of this function are listed bellow.
- `molecule`, the molecule object to add.
- `nx`, `ny`, `nz`, the number of molecules in x, y and z direction respectively.

`place_molecule_at`: place one molecule at a specific position. The required parameters of this function are listed bellow.
- `molecule`, the molecule object to add.
- `x`, `y`, `z`, the coordinate to place the molecule.

`enneutral`: place ions until the system is neutral. This function is only necessary when you run a simulation through Calvados-lc force field. No parameter is needed in this function.

`sub_box`: you can use this function to generate a simulation by combining existing boxes. The parameters are listed below.
- `sub_box`: the pre-existed simulation box to be placed in.
- `x`, `y`, `z`: the coordinate to place the `sub_box`.

#### analysis
Analysis module contains some operators for analyzing the simulation results. You can use these operators to get the information of the system, such as the temperature, the potential energy, the radius of gyration et al. These operators can be called by the `compute` function of a simulation box. Detailed information of each operator is listed as bellow.

`app.analysis.contact`: this function could calculate the contact map between two kinds of molecules. The function has three parameters.
- `type1`: the name of the first kind of molecule.
- `threshold`: if the distance between two CG beads is smaller than the threshold, the two CG beads are regarded as contact. Default is 4.
- `type2`: the name of the second kind of molecule. Default is '', which means the same as type1.

`app.analyse.momentum`
This function is an operator for computing the momentum of the system. No other parameters are needed. The function will return the momentum align x, y and z axe of the system.
Normally, the momentum of the system should be zero or very close to zero, None zero momentum indicates that the system is not correct, and you should rerun the simulation.

`app.analyse.temperature`
This function is an operator for computing the temperature of the system. No other parameters are needed. The function will return the temperature of the system.

`app.analyse.rg`
This function is an operator for computing the radius of gyration of the system. No other parameters are needed. The function will return the radius of gyration of the system.

`app.analyse.potential`
This function is an operator for computing the potential energy of the system. The simulation is needed as a parameter of this function. The function will return the potential energy of the system.
*Note:* before using this function, you must finish the simulation.

`app.analyse.rmsd`
This function is an operator for computing the root-mean-square deviation(RMSD) of the system. The function will return the RMSD of the system.

#### simulation
Simulation module contains the interaction potentials and the integrators. 
The first part of this module is the interaction potentials. The interaction potentials are used to describe the interactions between the CG beads. Generally, the parameters will be set automatically depending on the force field you use, and you don't need to set them manually. The available interaction potentials are listed below.
- `app.simulation.ah`:  Ashbaugh-Hatch potential.
- `app.simulation.bond_harmnic`: harmonic potential.
- `app.simulation.debye`: debye potential.
- `app.simulation.pppm`: pppm potential.
- `app.simulation.wf`: Wang-Frenkel potential.

The second part of this module is the integrators. You can choose which integrator to use in your simulation when creating your simulation. The available integrators are listed below. The parameters of the integrator are generated by the `env` of the app, and you don't need to set them manually. The available integrators are listed below.
- `app.simulation.langevin_nvt`: Langevin NVT integrator.
- `app.simulation.em`: NVE integrator, could be used for
- `app.simulation.noose_hover_nvt`: Noose Hover NVT integrator.
- `app.simulation.npt_z`: NPTMTK integrator. There is pressure coupling only in z direction.

#### sakuanna
Sakuanna is a sequence analysis module. It contains some functions for analyzing the sequence of the protein. Detailed information of each function is listed bellow.
`app.sakuanna.new_protein_sequence`: create a new protein sequence object. The function has three parameters.
- `fasta_path`: the path of the fasta file. If this parameter is set, the other two parameters will be ignored.
- `name`: the name of the protein. This parameter is needed when `fasta_path` is not set.
- `sequence`: the sequence of the protein. This parameter is needed when `fasta_path` is not set.
Depending on the sequences in the fasta file, the return value could be a list of protein sequence objects or a single protein sequence object.
example:
```python
seq1 = app.sakuanna.new_protein_sequence(
    fasta_path='input_data/proteins.fasta'
)
seq2 = app.sakuanna.new_protein_sequence(
    name='ELN',
    sequence='VPGAGVPGAGVPGAG'
)
```

`app.sakuanna.new_dna_sequence`: create a new DNA sequence object. The function has three parameters similar to `new_protein_sequence`.

`app.sakuanna.new_rna_sequence`: create a new RNA sequence object. The function has three parameters similar to `new_protein_sequence`.

`prettier`: this function can print the protein sequence in a prettier way. The function has three parameters.
- `protein`: the protein sequence object to print.
- `word3`: whether to print the sequence in three-letter code. Default is True.
- `ter`: whether to print the terminal group. Default is True.
example:
```python
sequence = app.sakuanna.new_protein_sequence(
    name='test',
    sequence='AAAAAAAAAAAAAAAAAAAAAAAA'
)
app.sakuanna.pretier(
    sequence, 
    word3=True, 
    ter=True
)
```

`statistics`: this function can calculate the ratio of specific amino acids in the protein sequence. The function has three parameters.
- `protein`: the protein sequence object to analyze.
- `targets`: the target amino acids or amino acid classes to analyze. The value could be a list of amino acids and amino acid classes. Available amino acid classes include `aromatic`, `positive`, `negative`, `charged`, `polar`, `nonpolar`. 
- `format_`: the format of the return value. Available values are `ratio` and `count`. If the value is `ratio`, the function will return the ratio of the target amino acids in the protein sequence. If the value is `count`, the function will return the count of the target amino acids in the protein sequence. Default is `ratio`.

example:
```python
res = app.sakuanna.statistic(
    sequence, 
    targets=['A', 'charged'],
    format_='ratio'
)
```

### data output
The output data of the analysis will be provided in from of an `AnalysisResult` object. You can do some operations on this object to change, view and save the data. The available functions are listed below.
- `print`: print the data in a prettier way.
- `distribution`: calculate the distribution of the exsited data. You can set `bins` of the distribution.
- `flatten`: calculate the average/total value of the data. The `action` parameter should be set. Available values include `average` and `sum`.
- `merge`: merge with other data.
- `normalize`: this function will normalize the data if the data is a vector.
- `plot`: show the plot of the data.
- `save`: save the data to `filename`.

### OmicsLoader
OmicsLoader is a module for loading omics data. This module will give you an easier experience in batch protein analysis. It can load data from various formats, such as fasta, pdb et al. You can use the functions provided by this module to load the data automatically.
To use this module, you need first to import OmicsLoader and batch_run. The first class is for reading the data you provide, while the second function is to dispatch the jobs of different proteins to different GPUs.
```python
from ipamd import OmicsLoader, batch_run
```
You first need to create an instance of OmicsLoader with the path of your data directory. Then you need to create a function to process the data. The function should have two parameters, the first parameter is the app, and the second one is data. These two parameters will be passed by the batch_run function. The data parameter is a dictionary, which contains the name, sequence, type and path of the data. A detailed example is shown below.
```python
loader = OmicsLoader(path='input_data/transcription')
def process_sequence(app, data):
    app.use('Calvados3')
    box = app.builder.new_simulation_box(150, 150, 150)
    mol = app.builder.protein_from_pdb(
        data['name'] + '.pdb', 
        rigid_from_plddt=True
    )
    box.place_molecule_periodically(mol, 1, 1, 1)
    simulation = app.simulation.new_simulation(
        box,
        f'{data['name']}', 
        total_time=20 * Unit.TimeScale.ns, 
        snap_shot=100
    )
    simulation.run('n')
    flory = box.compute(
        app.analysis.flory_monomer, 
        title='flory', 
        target_frame='50-100'
    )
    flory.print()
    with open('results.csv', 'a') as f:
        f.write(f'{data["name"]},{flory.data}\n')

batch_run(loader, process_sequence)
```

### configuration
The config file of this package is located at `~/.local/ipamd/config.json`. The configuration file will be created when you first run this package. You can modify the configuration file to change the behavior of the package, such as the path of the data file, the path of extra plugins, and the path of the output file, et al. The detailed configuration items are listed below.

| Item         | Description                           | Available values                                                                                         |
|--------------|---------------------------------------|----------------------------------------------------------------------------------------------------------|
| result_dir   | where to write the simulation results | the target directory, or set to `$decentralized` if you don't want to get your output managed by IPAMD   |
| output_level | how much log is printed               | 0: verbose, 1: info, 2: warning, 3: error                                                                |
| auto_load    | whether to load the plugins automatically | True or False                                                                                            |
| sakuanna_plugin_dir | the path of extra sakuanna plugins | a list of target directories                                                                             |
| simulation_plugin_dir | the path of extra simulation plugins | a list of target directories                                                                             |
| builder_plugin_dir | the path of extra builder plugins | a list of target directories                                                                             |
| analyse_plugin_dir | the path of extra analyse plugins | a list of target directories                                                                             |
| default_ff  | the default force field               | the name of the force field, should be one of the available force fields printed by `app.available_ff()` |

### examples
Some example code is provided in the demo folder. You can run these examples to get familiar with this package. There are some subfolders in the demo folder, each subfolder contains an example code and the input data needed. The meaning of the examples could refer to the paper of this package(doi: 10.1021/acs.jctc.5c00147).

## Second-time-development
IPAMD is a plugin-based software, and the developer could easily add new functions to this package by writing a plugin. The detailed instruction on writing a plugin is shown in this section.

### Plugin
A plugin is a Python module that contains one or more classes or functions. There should be a function named `func`, and this func will be detected and loaded by IPAMD automatically. There is a configuration variable for each plugin. This variable looks like:
```python
configure = {
    'type': 'function',
    "schema": 'schema_name',
    "apply": ['applied_value']
}
```
The `type` variable is deprecated and will be removed in future versions. The only available value is `function`. The `apply` variable indicates which value should be passed to the plugin. Your function should also have a parameter that has the same name with the applied value. The `schema` variable indicates a combination of applied value. But the schema variable is not necessary in most cases and not recommended for developers.

You can also call another plugin in your plugin. To do this, you need to import the `PluginBase` class from `ipamd.public.utils`, and then use `PluginBase.call('plugin_name', parameters)` to call the target plugin. The `plugin_name` is the name of the plugin you want to call, and the `parameters` is a dict that contains the parameters needed by the target plugin. *Note: This feature is beta and may be not stable.*

## Supporting
Contact me at [email](mailto:liuxiaoyang_Q@outlook.com) if you have any questions or suggestions. You can also submit an issue on the GitHub page. I will reply to you as soon as possible.