# GptCloneBench
GPTCloneBench is a clone detection benchmark based on SemanticCloneBench [1] and GPT [2,3,4,5]. This work is accepted at ICSME2023 conference.

Please find the benchmark here: https://shorturl.at/owxJM

## System requirement

To install necessary libraries, please run the following command:

```
pip install -r requirements.txt
```

To run NiCad on generated Clone, you need to install TXL and NiCad.

- Download TXL from this URL: http://txl.ca/txl-download.html
- Download NiCad from this URL: http://txl.ca/txl-nicaddownload.html

To generate clones, you need to have SemanticCloneBench [1]. Follow this link to download SemanticCloneBench: https://drive.google.com/open?id=1KicfslV02p6GDPPBjZHNlmiXk-9IoGWl

To manually validate GPT clones, we have utilized tool from Jeffrey Svajlenko: https://github.com/jeffsvajlenko/ValidateClones

You need OpenAI API key to run the system. This link provided details on how to obtain OpenAI API key: https://www.maisieai.com/help/how-to-get-an-openai-api-key-for-chatgpt

Please follow the link to generate your own secret API key.

## Generate and validate GPTCloneBench

To generate semantic clone, follow the following steps:

1. Clone this repository.
2. Copy SemanticCloneBench into this folder.
3. run `python create_clones_for_gptclonebench.py`. Follow the prompts to generate clones.
4. run `python file_creation_for_validateClones.py` to create input file for manual validation.
5. run `python crossL_file_creation_for_validateClones.py` to create input file for manual validation for cross language clones.


## Benchmark Validator (Undergraduate Interns):
  
  1. Chi Phuong Vu
     
     GitHub ID: 115325256, Email: chi.vu@usask.ca

  2. Olaoluwa Dayo-Olaide
     
     Email: pla326@usask.ca

  3. Souvik Ukil
  
     Email: fgb792@mail.usask.ca

  4. Aryan Mehta
     
     GitHub ID: 90737338, Email: gmj287@mail.usask.ca or aryanmht9@gmail.com

  5. Dipika Ayshi
     
     Email: dipikaayshi@gmail.com

  6. Jayse Cai
     
     Email: ctc261@mail.usask.ca

## License
Benchmark: The benchmark is distributed under the Creative Commons, Attribution-NonCommercial-NoDerivatives.  This license includes the benchmark database and its derivatives.  For attribution, please cite this page, and our publications below.  This data is provided free of charge for non-commercial and academic benchmarking and experimentation use.  If you would like to contribute to the benchmark, please contact us.  If you believe you intended usage may be restricted by the license, please contact us and we can discuss the possibilities.
BibTex for the GPTCloneBench (initial version):

```
@inproceedings{gptclonebench2023,
  title={GPTCloneBench: A comprehensive benchmark of semantic clones and cross-language clones using GPT-3 model and SemanticCloneBench},
  author={Alam, Ajmain Inqiad and Roy, Palash Ranjan and Al-omari, Farouq and Roy, Chanchal Kumar and Roy, Banani and Schneider, Kevin},
  booktitle={Proceedings of the 39th International Conference in Software Maintenance and Evolution (ICSME 2023)},
  year={2023},
  organization={October 2023, Bogota, Colombia (to appear)}
}
```

## Contact

Ajmain Inqiad Alam: ajmain.alam@usask.ca / ajmaininqiadalam@gmail.com

Palash Ranjan Roy: palash.roy@usask.ca / palash.roy101@gmail.com

Farouq Al-omari: faa634@usask.ca

Chanchal K. Roy: chanchal.roy@usask.ca

Banani Roy: banani.roy@usask.ca

Kevin Schneider: kevin.schneider@usask.ca



## BibTeX Citation
```
1. @inproceedings{al2020semanticclonebench,
    title={Semanticclonebench: A semantic code clone benchmark using crowd-source knowledge},
    author={Al-Omari, Farouq and Roy, Chanchal K and Chen, Tonghao},
    booktitle={2020 IEEE 14th International Workshop on Software Clones (IWSC)},
    pages={57--63},
    year={2020},
    organization={IEEE}
  }

2. @article{brown2020language,
    title={Language models are few-shot learners},
    author={Brown, Tom and Mann, Benjamin and Ryder, Nick and Subbiah, Melanie and Kaplan, Jared D and Dhariwal, Prafulla and Neelakantan, Arvind and Shyam, Pranav and Sastry, Girish and Askell, Amanda and others},
    journal={Advances in neural information processing systems},
    volume={33},
    pages={1877--1901},
    year={2020}
}

3. @misc{morrison_2022, 
    title={GPT-3 developer OpenAI releases new Davinci Generative Text Model}, 
    url={https://techmonitor.ai/technology/ai-and-automation/gpt-3-openai-davinci-generative-text}, 
    journal={Tech Monitor}, 
    author={Morrison, Ryan}, 
    year={2022}, 
    month={Nov}
 }

4. @misc{jain_2022,
    title={OpenAI turns to Davinci to make GPT-3 Better},
    url={https://analyticsindiamag.com/openai-turns-to-davinci-to-make-gpt-3-better/},
    journal={Analytics India Magazine},
    author={Jain, Ayush},
    year={2022},
    month={Nov}
} 

5. @misc{monge_2022,
    title={New GPT-3 model: Text-DAVINCI-003 is awesome},
    url={https://medium.com/technology-hits/new-gpt-3-model-text-davinci-003-is-awesome-ada11ef660a9},
    journal={Medium},
    publisher={Technology Hits},
    author={Monge, Jim Clyde},
    year={2022},
    month={Dec}
} 
```

