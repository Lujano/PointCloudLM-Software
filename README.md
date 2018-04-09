# PointCloudLM-Software
Software empleado en la implementación del sistema de generación de nubes de puntos

La descripción de las librerias empleadas se encuentra en [PointCloudLM-Software Wiki](https://github.com/Lujano/PointCloudLM-Software/wiki)



![](https://github.com/Lujano/PointCloudLM-Software/blob/master/Install/Install3.png  )


# Prerrequisitos
Este proyecto se realizó en un ambiente de Anaconda 4.3.30  nombrado como PointCloudLM

Para instalar Anaconda, diriijase a su  [página de descarga](https://www.anaconda.com/download/).

# Instalación del ambiente PointCloudLM para Windows y Linux
* Una vez instalado Anaconda, abrir el prompt de anaconda y ejecutar el siguiente comando:
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
Se deben instalar las librerias flask, flask-wtf, requests para poder ejecutar los codigos finales del proyecto en los  que se emplea comunicacion WIFI.
## IDE Python

En nuestro proyecto se empleo Pycharm como IDE de desarrollo:

Para instalar Pycharm, dirijase a su  [página de descarga](https://www.jetbrains.com/pycharm/download/)

Las librerias restantes (flask, flask-wtf, requests) se pueden instalar desde el IDE de Anaconda en el panel de configuracion:

![](https://github.com/Lujano/PointCloudLM-Software/blob/master/Install/Install.png)


![](https://github.com/Lujano/PointCloudLM-Software/blob/master/Install/Install2.png)



