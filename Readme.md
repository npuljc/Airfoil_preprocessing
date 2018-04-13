# Python scripts for preprocessing UIUC airfoils

## Usage
This repo contains three python scripts to preprocess airfoil data files in the [UIUC airfoil database](http://m-selig.ae.illinois.edu/ads/coord_database.html).
You need download the airfoil data from that website. Then you can run the scripts one by one:

- Step 1: Format Data. Remove unnesessary texts from the files and eliminate incomplete airfoils.
- Step 2: Uniform Data. Sharpen airfoils' trailing edges and uniform them.
- Step 3: Select Data. Remove non-smooth airfoils.

After these treatments, you will obtain 1458 UIUC airfoils of the same format.

## Licensing
Distributed using the GNU Lesser General Public License (LGPL); see the LICENSE file for details.

Just a polite request, please cite the author's papers listed below for which you find it useful.

- A data-based approach for fast airfoil analysis and optimization, 2018 AIAA SciTech Conference, DOI: [10.2514/6.2018-1383](https://doi.org/10.2514/6.2018-1383)
- Data-driven Geometry Constraints for High-Fidelity Aerodynamic Shape Optimization

## Contact and Feedback
If you have questions, comments, problems, or want to report a bug, please contact the author:

Jichao Li (cfdljc@gmail.com)




