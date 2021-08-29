import PyInstaller.__main__

PyInstaller.__main__.run([
	'src/main.py',
	# '--onefile',
	'--noconsole',
	'--add-data=src/*:.',
	'--add-data=src/modules/*:.',
	'--hidden-import=PILLOW',
	'--hidden-import=PIL',
])
