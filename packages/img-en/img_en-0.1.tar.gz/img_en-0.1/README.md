# image-enlarge
It takes img and int zoom level and output zoomed image.

##Installation
```pip install img_en```

## How to use it?

## Example
  ```
   import img_en
   #importing module

   img = img_en.load("image.jpg")
   #loading image

   zoom = 2 
   #declaring int value for level of zoom

   zoomimg = img_en.enlarge(img,zoom) 
   #zooming image

   img_en.save("zoomimage.jpg",zoomimg)
   #saving zoom image 

   img_en.show("title",zoomimg)
   #displaying image

   img_en.wait(0)
   #0 for stop
   #1 for don't stop
