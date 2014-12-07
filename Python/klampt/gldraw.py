"""OpenGL drawing functions for geometric primitives."""

import math
import vectorops
import se3
import ctypes
from OpenGL.GL import *
from OpenGL.GLUT import *

def point(p):
    glBegin(GL_POINTS)
    if len(p)==2:
        glVertex2f(*p)
    elif len(p)==3:
        glVertex3f(*p)
    else:
        glVertex3f(p[0],p[1],p[2])
    glEnd()

def circle(center,radius,res=0.01):
    numdivs = int(math.ceil(radius*math.pi*2/res))
    glNormal3f(0,0,1)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(*center)
    for i in xrange(numdivs+1):
        u = float(i)/float(numdivs)*math.pi*2
        glVertex2f(center[0]+radius*math.cos(u),center[1]+radius*math.sin(u))
    glEnd()

def triangle(a,b,c,lighting=True):
    if lighting:
        n = vectorops.cross(vectorops.sub(b,a),vectorops.sub(c,a))
        n = vectorops.mul(n,1.0/vectorops.norm(n))
        glNormal3f(*n)
    glBegin(GL_TRIANGLES)
    glVertex3f(*a)
    glVertex3f(*b)
    glVertex3f(*c)
    glEnd();


def quad(a,b,c,d,lighting=True):
    if lighting:
        n = vectorops.cross(vectorops.sub(b,a),vectorops.sub(c,a))
        n = vectorops.mul(n,1.0/vectorops.norm(n))
        glNormal3f(*n)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(*a)
    glVertex3f(*b)
    glVertex3f(*c)
    glVertex3f(*d)
    glEnd();

def box(a=(0,0,0),b=(1,1,1),lighting=True):
    quad((a[0], a[1], a[2]),
         (a[0], b[1], a[2]),
         (b[0], b[1], a[2]),
         (b[0], a[1], a[2]),lighting)
    quad((a[0], a[1], b[2]),
         (b[0], a[1], b[2]),
         (b[0], b[1], b[2]),
         (a[0], b[1], b[2]),lighting)
    quad((a[0], a[1], a[2]),
         (a[0], a[1], b[2]),
         (a[0], b[1], b[2]),
         (a[0], b[1], a[2]),lighting)
    quad((b[0], a[1], a[2]),
         (b[0], b[1], a[2]),
         (b[0], b[1], b[2]),
         (b[0], a[1], b[2]),lighting)
    quad((a[0], a[1], a[2]),
         (b[0], a[1], a[2]),
         (b[0], a[1], b[2]),
         (a[0], a[1], b[2]),lighting)
    quad((a[0], b[1], a[2]),
         (a[0], b[1], b[2]),
         (b[0], b[1], b[2]),
         (b[0], b[1], a[2]),lighting)

def centered_box(dims=(1,1,1),lighting=True):
    box([-d*0.5 for d in dims],[d*0.5 for d in dims],lighting)

def setcolor(r,g,b,a=1.0,lighting=True):
    if lighting:
        glMaterialfv(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE,[r,g,b,a])
    else:
        glColor4f(r,g,b,a)

def xform_widget(T,length,width,lighting=True):
    mat = zip(*se3.homogeneous(T))
    mat = sum([list(coli) for coli in mat],[])

    glPushMatrix()
    glMultMatrixf(mat)

    #center
    setcolor(1,1,1,1,lighting=lighting)
    box((-width*0.75,-width*0.75,-width*0.75),(width*0.75,width*0.75,width*0.75),lighting=lighting)

    #x axis
    setcolor(1,0,0,1,lighting=lighting)
    box((-width*0.5,-width*0.5,-width*0.5),(length,width*0.5,width*0.5),lighting=lighting)
    
    #y axis
    setcolor(0,1,0,1,lighting=lighting)
    box((-width*0.5,-width*0.5,-width*0.5),(width*0.5,length,width*0.5),lighting=lighting)
    
    #z axis
    setcolor(0,0,1,1,lighting=lighting)
    box((-width*0.5,-width*0.5,-width*0.5),(width*0.5,width*0.5,length),lighting=lighting)
    
    glPopMatrix()

def glutBitmapString(font,string):
    for c in string:
        glutBitmapCharacter(font,ctypes.c_int(ord(c)))
