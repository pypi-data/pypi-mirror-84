import setuptools
import io

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Python-EasyGraph",                                     
    version="0.2a14",                                        
    author="Fudan MSN Group",                                       
    author_email="easygraph@163.com",                      
    description="Easy Graph",                            
    long_description=long_description,                      
    long_description_content_type="text/x-rst",          
    url="https://github.com/easy-graph/Easy-Graph",                              
    packages=setuptools.find_packages(),                    
    classifiers=[                                           
        "Programming Language :: Python :: 3",              
        "License :: OSI Approved :: BSD License",           
        "Operating System :: OS Independent",               
    ],
    python_requires=">=3.6,<3.8",
    install_requires=['numpy','tqdm','tensorflow>=2.0.0','joblib',
    'six','gensim','progressbar33','scikit-learn','scipy',
    ]
)

