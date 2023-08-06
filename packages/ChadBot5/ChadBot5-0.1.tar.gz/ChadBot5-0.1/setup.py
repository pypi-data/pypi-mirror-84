import setuptools


setuptools.setup(
    name = "ChadBot5",
    version = "0.1",
    author = "Rushi Babaria",
    url = "https://github.com/captanlevi/FAQ-QnA-matching.git",
    packages = setuptools.find_packages(),
    install_requires = ["sentence_transformers==0.3.8","pandas", "numpy","regex","nlpaug","spacy", "tqdm"]
)

