from setuptools import setup, find_packages

setup(name='PyAmdecoder', # 프로젝트 이름
      version='0.0.1', # 프로젝트 버전
      url='https://github.com/harry595/Py_Amdecoder', # 프로젝트 주소
      license='MIT',
      author='harry595', # 작성자
      author_email='harry919@ajou.ac.kr', # 작성자 이메일
      description='AndroidManifest.xml PyDecoder', # 간단한 설명
      packages=find_packages(exclude=['']),  # 기본 프로젝트 폴더 외에 추가로 입력할 폴더
      long_description=open('README.md').read(), # 프로젝트 설명, 보통 README.md로 관리
      install_requires=[''], # 설치시 설치할 라이브러리
)