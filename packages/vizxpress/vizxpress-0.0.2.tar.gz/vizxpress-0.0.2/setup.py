import setuptools


setuptools.setup(
    name='vizxpress',
    version='0.0.2',
    packages=setuptools.find_packages(),
    # data_files=[(['VizXpress/gsea_databases/all_curated_genesets.gmt', 'VizXpress/gsea_databases/immunological_signatures.gmt',
    #                                'VizXpress/gsea_databases/msigdb_hallmarks.gmt', 'VizXpress/gsea_databases/reactomeconda _canonical_pathways.gmt'])],
    python_requires='>=3.6',
    url='',
    license='GNU Affero General Public License v3.0',
    author='Colton J. Garelli',
    author_email='',
    description='A unified set of analysis and visualization tools intended for gene expression studies in Python')
