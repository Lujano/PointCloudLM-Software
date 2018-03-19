# PointCloud-Software
Software empleado en la implementación del sistema de generación de nubes de puntos

# Prerrequisitos
Este proyecto se realizó en un ambiente de Anaconda 4.3.30 llamado PointCloudLM

Para instalar Anaconda, dirgirse a su  [página de descarga](https://www.anaconda.com/download/).

# Instalación del ambiente PointCloudLM
* Una vez instalado Anaconda, abrir el prompt y ejecutar el siguiente comando:
```bash
conda create --name PointCloudLM --channel ccordoba12 pcl python-pcl matplotlib mayavi numpy pyserial scipy
```

Lo cual instala python 2.7 y las librerias pcl, matplotlib, mayavi y numpy pyserial y scipy

* Luego, se procede a activar el ambiente:

```bash
activate  PointCloudLM
```
* y se instala la libreria de opencv:

```bash
pip install opencv-python
```
* Se chequea que opencv este instalado:

```bash
python import cv2
```

crlt+q para salir

* y se desactiva el environment:
```bash
deactivate
```
## IDE Python

En nuestro proyecto se empleo Pycharm como IDE de desarrollo:

https://www.jetbrains.com/pycharm/download/

