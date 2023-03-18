"""Script to extract cross section data from Lib80x data. 
For correct execution, run this script from within the trinidi/data directory.

The Lib80x data is available at https://nucleardata.lanl.gov/ace/lib80x/"""

import os
import openmc.data 
import numpy as np

available_isotopes = ['H-1', 'H-2', 'H-3', 'He-3', 'He-4', 'Li-6', 'Li-7', 'Be-7', 'Be-9', 'B-11', 'C-12', 'C-13', 'N-14', 'N-15', 'O-16', 'O-17', 'O-18', 'F-19', 'Ne-20', 'Ne-21', 'Ne-22', 'Na-22', 'Na-23', 'Mg-24', 'Mg-25', 'Mg-26', 'Al-27', 'Si-28', 'Si-29', 'Si-30', 'Si-31', 'Si-32', 'P-31', 'S-32', 'S-33', 'S-34', 'S-35', 'S-36', 'Cl-35', 'Cl-36', 'Cl-37', 'Ar-36', 'Ar-37', 'Ar-38', 'Ar-39', 'Ar-40', 'Ar-41', 'K-39', 'K-40', 'K-41', 'Ca-40', 'Ca-41', 'Ca-42', 'Ca-43', 'Ca-44', 'Ca-45', 'Ca-46', 'Ca-47', 'Ca-48', 'Sc-45', 'Ti-46', 'Ti-47', 'Ti-48', 'Ti-49', 'Ti-50', 'V-49', 'V-50', 'V-51', 'Cr-50', 'Cr-51', 'Cr-52', 'Cr-53', 'Cr-54', 'Mn-54', 'Mn-55', 'Fe-54', 'Fe-55', 'Fe-56', 'Fe-57', 'Fe-58', 'Co-58', 'Co-59', 'Ni-58', 'Ni-59', 'Ni-60', 'Ni-61', 'Ni-62', 'Ni-63', 'Ni-64', 'Cu-63', 'Cu-64', 'Cu-65', 'Zn-64', 'Zn-65', 'Zn-66', 'Zn-67', 'Zn-68', 'Zn-69', 'Zn-70', 'Ga-69', 'Ga-70', 'Ga-71', 'Ge-70', 'Ge-71', 'Ge-72', 'Ge-73', 'Ge-74', 'Ge-75', 'Ge-76', 'As-73', 'As-74', 'As-75', 'Se-74', 'Se-75', 'Se-76', 'Se-77', 'Se-78', 'Se-79', 'Se-80', 'Se-81', 'Se-82', 'Br-79', 'Br-80', 'Br-81', 'Kr-78', 'Kr-79', 'Kr-80', 'Kr-81', 'Kr-82', 'Kr-83', 'Kr-84', 'Kr-85', 'Kr-86', 'Rb-85', 'Rb-86', 'Rb-87', 'Sr-84', 'Sr-85', 'Sr-86', 'Sr-87', 'Sr-88', 'Sr-89', 'Sr-90', 'Y-89', 'Y-90', 'Y-91', 'Zr-90', 'Zr-91', 'Zr-92', 'Zr-93', 'Zr-94', 'Zr-95', 'Zr-96', 'Nb-93', 'Nb-94', 'Nb-95', 'Mo-92', 'Mo-93', 'Mo-94', 'Mo-95', 'Mo-96', 'Mo-97', 'Mo-98', 'Mo-99', 'Mo-100', 'Tc-98', 'Tc-99', 'Ru-96', 'Ru-97', 'Ru-98', 'Ru-99', 'Ru-100', 'Ru-101', 'Ru-102', 'Ru-103', 'Ru-104', 'Ru-105', 'Ru-106', 'Rh-103', 'Rh-104', 'Rh-105', 'Pd-102', 'Pd-103', 'Pd-104', 'Pd-105', 'Pd-106', 'Pd-107', 'Pd-108', 'Pd-109', 'Pd-110', 'Ag-107', 'Ag-108', 'Ag-109', 'Ag-111', 'Ag-112', 'Ag-113', 'Ag-114', 'Ag-115', 'Ag-116', 'Ag-117', 'Cd-106', 'Cd-107', 'Cd-108', 'Cd-109', 'Cd-110', 'Cd-111', 'Cd-112', 'Cd-113', 'Cd-114', 'Cd-116', 'In-113', 'In-114', 'In-115', 'Sn-112', 'Sn-113', 'Sn-114', 'Sn-115', 'Sn-116', 'Sn-117', 'Sn-118', 'Sn-119', 'Sn-120', 'Sn-122', 'Sn-123', 'Sn-124', 'Sn-125', 'Sn-126', 'Sb-121', 'Sb-122', 'Sb-123', 'Sb-124', 'Sb-125', 'Sb-126', 'Te-120', 'Te-121', 'Te-122', 'Te-123', 'Te-124', 'Te-125', 'Te-126', 'Te-128', 'Te-130', 'Te-131', 'Te-132', 'I-127', 'I-128', 'I-129', 'I-130', 'I-131', 'I-132', 'I-133', 'I-134', 'I-135', 'Xe-123', 'Xe-124', 'Xe-125', 'Xe-126', 'Xe-127', 'Xe-128', 'Xe-129', 'Xe-130', 'Xe-131', 'Xe-132', 'Xe-133', 'Xe-134', 'Xe-135', 'Xe-136', 'Cs-133', 'Cs-134', 'Cs-135', 'Cs-136', 'Cs-137', 'Ba-130', 'Ba-131', 'Ba-132', 'Ba-133', 'Ba-134', 'Ba-135', 'Ba-136', 'Ba-137', 'Ba-138', 'Ba-139', 'Ba-140', 'La-138', 'La-139', 'La-140', 'Ce-136', 'Ce-137', 'Ce-138', 'Ce-139', 'Ce-140', 'Ce-141', 'Ce-142', 'Ce-143', 'Ce-144', 'Pr-141', 'Pr-142', 'Pr-143', 'Nd-142', 'Nd-143', 'Nd-144', 'Nd-145', 'Nd-146', 'Nd-147', 'Nd-148', 'Nd-149', 'Nd-150', 'Pm-143', 'Pm-144', 'Pm-145', 'Pm-146', 'Pm-147', 'Pm-148', 'Pm-149', 'Pm-150', 'Pm-151', 'Sm-144', 'Sm-145', 'Sm-146', 'Sm-147', 'Sm-148', 'Sm-149', 'Sm-150', 'Sm-151', 'Sm-152', 'Sm-153', 'Sm-154', 'Eu-151', 'Eu-152', 'Eu-153', 'Eu-154', 'Eu-155', 'Eu-156', 'Eu-157', 'Gd-152', 'Gd-153', 'Gd-154', 'Gd-155', 'Gd-156', 'Gd-157', 'Gd-158', 'Gd-159', 'Gd-160', 'Tb-158', 'Tb-159', 'Tb-160', 'Tb-161', 'Dy-154', 'Dy-155', 'Dy-156', 'Dy-157', 'Dy-158', 'Dy-159', 'Dy-160', 'Dy-161', 'Dy-162', 'Dy-163', 'Dy-164', 'Ho-165', 'Er-162', 'Er-163', 'Er-164', 'Er-165', 'Er-166', 'Er-167', 'Er-168', 'Er-169', 'Er-170', 'Tm-168', 'Tm-169', 'Tm-170', 'Tm-171', 'Yb-168', 'Yb-169', 'Yb-170', 'Yb-171', 'Yb-172', 'Yb-173', 'Yb-174', 'Yb-175', 'Yb-176', 'Lu-175', 'Lu-176', 'Hf-174', 'Hf-175', 'Hf-176', 'Hf-177', 'Hf-178', 'Hf-179', 'Hf-180', 'Hf-181', 'Hf-182', 'Ta-180', 'Ta-181', 'Ta-182', 'W-180', 'W-181', 'W-182', 'W-183', 'W-184', 'W-185', 'W-186', 'Re-185', 'Re-187', 'Os-184', 'Os-185', 'Os-186', 'Os-187', 'Os-188', 'Os-189', 'Os-190', 'Os-191', 'Os-192', 'Ir-191', 'Ir-192', 'Ir-193', 'Pt-190', 'Pt-191', 'Pt-192', 'Pt-193', 'Pt-194', 'Pt-195', 'Pt-196', 'Pt-197', 'Pt-198', 'Au-197', 'Hg-196', 'Hg-197', 'Hg-198', 'Hg-199', 'Hg-200', 'Hg-201', 'Hg-202', 'Hg-203', 'Hg-204', 'Tl-203', 'Tl-204', 'Tl-205', 'Pb-204', 'Pb-205', 'Pb-206', 'Pb-207', 'Pb-208', 'Bi-209', 'Po-208', 'Po-209', 'Po-210', 'Ra-223', 'Ra-224', 'Ra-225', 'Ra-226', 'Ac-225', 'Ac-226', 'Ac-227', 'Th-227', 'Th-228', 'Th-229', 'Th-230', 'Th-231', 'Th-232', 'Th-233', 'Th-234', 'Pa-229', 'Pa-230', 'Pa-231', 'Pa-232', 'Pa-233', 'U-230', 'U-231', 'U-232', 'U-233', 'U-234', 'U-235', 'U-236', 'U-237', 'U-238', 'U-239', 'U-240', 'U-241', 'Np-234', 'Np-235', 'Np-236', 'Np-237', 'Np-238', 'Np-239', 'Pu-236', 'Pu-237', 'Pu-238', 'Pu-239', 'Pu-240', 'Pu-241', 'Pu-242', 'Pu-243', 'Pu-244', 'Pu-245', 'Pu-246', 'Am-240', 'Am-241', 'Am-242', 'Am-243', 'Am-244', 'Cm-240', 'Cm-241', 'Cm-242', 'Cm-243', 'Cm-244', 'Cm-245', 'Cm-246', 'Cm-247', 'Cm-248', 'Cm-249', 'Cm-250', 'Bk-245', 'Bk-246', 'Bk-247', 'Bk-248', 'Bk-249', 'Bk-250', 'Cf-246', 'Cf-247', 'Cf-248', 'Cf-249', 'Cf-250', 'Cf-251', 'Cf-252', 'Cf-253', 'Cf-254', 'Es-251', 'Es-252', 'Es-253', 'Es-254', 'Es-255', 'Fm-255']
z_numbers = {'H': 1,'He': 2,'Li': 3,'Be': 4,'B': 5,'C': 6,'N': 7,'O': 8,'F': 9,'Ne': 10,'Na': 11,'Mg': 12,'Al': 13,'Si': 14,'P': 15,'S': 16,'Cl': 17,'Ar': 18,'K': 19,'Ca': 20,'Sc': 21,'Ti': 22,'V': 23,'Cr': 24,'Mn': 25,'Fe': 26,'Co': 27,'Ni': 28,'Cu': 29,'Zn': 30,'Ga': 31,'Ge': 32,'As': 33,'Se': 34,'Br': 35,'Kr': 36,'Rb': 37,'Sr': 38,'Y': 39,'Zr': 40,'Nb': 41,'Mo': 42,'Tc': 43,'Ru': 44,'Rh': 45,'Pd': 46,'Ag': 47,'Cd': 48,'In': 49,'Sn': 50,'Sb': 51,'Te': 52,'I': 53,'Xe': 54,'Cs': 55,'Ba': 56,'La': 57,'Ce': 58,'Pr': 59,'Nd': 60,'Pm': 61,'Sm': 62,'Eu': 63,'Gd': 64,'Tb': 65,'Dy': 66,'Ho': 67,'Er': 68,'Tm': 69,'Yb': 70,'Lu': 71,'Hf': 72,'Ta': 73,'W': 74,'Re': 75,'Os': 76,'Ir': 77,'Pt': 78,'Au': 79,'Hg': 80,'Tl': 81,'Pb': 82,'Bi': 83,'Po': 84,'At': 85,'Rn': 86,'Fr': 87,'Ra': 88,'Ac': 89,'Th': 90,'Pa': 91,'U': 92,'Np': 93,'Pu': 94,'Am': 95,'Cm': 96,'Bk': 97,'Cf': 98,'Es': 99,'Fm': 100,'Md': 101,'No': 102,'Lr': 103,'Rf': 104,'Db': 105,'Sg': 106,'Bh': 107,'Hs': 108,'Mt': 109}

def get_file_name(isotope, z_numbers, data_dir):
    """Get file name pointing to x-sec and energy data

        isotope (str): isotope name.
        z_numbers: dictionary mapping isotopes to z-numbers.
        data_dir: directory of Lib80x data.

    """
    symbol, A = isotope.split('-')
    A = int(A)
    Z = z_numbers[symbol]
    ZA = Z * 1000 + A;
    base_name = str(ZA) + ".800nc"
    file_name = data_dir + "/" + symbol + "/" + base_name
    return base_name, file_name


def read_file(file_name):
    """Read energy (eV) and cross section (barns)
    
    """
    lib = openmc.data.IncidentNeutron.from_ace(file_name)
    total = lib[1] # <Reaction: MT=1 (n,total)>
    energy = lib.energy['294K']
    cross_section = total.xs['294K'](energy)
    return energy, cross_section



data_dir = input("Lib80x directory: ")

if(not os.path.exists(data_dir)):
    raise Exception(f'data_dir: `{data_dir}` does not exist')


isotopes = available_isotopes
energies = []
cross_sections = []
basenames = []


print('Processing ...')
for i, iso in enumerate(isotopes):

    base_name, file_name = get_file_name(iso, z_numbers, data_dir)

    print(f'{iso}, file name: {base_name}')

    if(not os.path.exists(file_name)):
        raise Exception(f'file_name: `{file_name}` does not exist')

    energy, cross_section = read_file(file_name)

    energies.append(energy)
    cross_sections.append(cross_section)
    basenames.append(base_name)


xsdata = {'isotopes': isotopes, 'energies': energies, 'cross_sections': cross_sections, 'Lib80x_file_name': basenames}
np.save('xsdata.npy', xsdata, allow_pickle=True)







