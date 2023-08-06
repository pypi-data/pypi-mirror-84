from setuptools import setup, find_packages 

with open('requirements.txt') as f: 
	requirements = f.readlines() 

long_description = 'Uses gstreamer(playsound) as backend' 

setup( 
		name ='ytstreamer', 
		version ='1.1.1', 
		author ='Icelain', 
		author_email ='xerneas965@gmail.com', 
		url ='https://github.com/Icelain/YTStreamer', 
		description ='Script that streams music (or audio) from youtube', 
		long_description = long_description, 
		long_description_content_type ="text/markdown", 
		license ='MIT', 
		packages = find_packages(), 
		entry_points ={ 
			'console_scripts': [ 
				'ytstream = src.streamer:main'
			] 
		}, 
		classifiers =( 
			"Programming Language :: Python :: 3", 
			"License :: OSI Approved :: MIT License", 
			"Operating System :: OS Independent", 
		), 
		keywords ='music streaming youtube audio audiostream youtubestream script', 
		install_requires = requirements, 
		zip_safe = False
) 
