import setuptools

with open ( "README.md" , "r",encoding='UTF-8' ) as fh :
    long_description = fh.read()

setuptools . setup (
    name = "jsonpath-kv" ,
    version = "0.0.8" ,
    author = "Wanghao" ,
    author_email = "947001731@qq.com" ,
    description = "Gets the value in the JSON data" ,
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = "https://github.com/WangHaoz/jsonpath-kv" ,
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3" ,
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent" ,
    ],
)