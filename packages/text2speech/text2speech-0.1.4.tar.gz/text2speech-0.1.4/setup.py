from setuptools import setup

setup(
    name='text2speech',
    version='0.1.4',
    packages=['text2speech', 'text2speech.modules'],
    url='https://github.com/HelloChatterbox/text2speech',
    license='apache2',
    install_requires=["jarbas_utils",
                      "requests_futures",
                      "boto3",
                      "ResponsiveVoice",
                      "psutil",
                      "gTTS>=2.0.3",
                      "gTTS-token>=1.1.3",
                      "voxpopuli"],
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='TTS engines'
)
