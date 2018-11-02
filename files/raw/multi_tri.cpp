#include <GL/gl.h>
#include <GL/glut.h>   // freeglut.h might be a better alternative, if available.

float x1=-0.4,x2=0.4,x3=0;
float y1=0.0,y2=0.0,y3=-0.9;

void draww(float x1,float x2,float x3,float y1,float y2,float y3,int level){
    if(level==0)
        return;
    glBegin(GL_TRIANGLES);
    glColor3f( 0, 0, 1 ); // red
    glVertex2f( x1, y1 );
    glColor3f( 0, 0, 1 ); // green
    glVertex2f( x2, y2 );
    glColor3f( 0, 0, 1 ); // blue
    glVertex2f( x3, y3 );
    glEnd(); 
    float a,b,c,a1,b1,c1;
    a=x1+x2;
    a/=2;
    b=x1+a;
    b/=2;
    c=a+x2;
    c/=2;
    b1=(y2-y3)/2;
    b1=y2+b1;
    draww(b,c,x3,b1,b1,y2,level-1);
    a=(x3-x1)/2;
    b=x1-a;
    c=x1+a;
    b1=(y1+y3)/2;
    draww(b,c,x1,b1,b1,y3,level-1);
    b=x2-a;
    c=x2+a;
    draww(b,c,x2,b1,b1,y3,level-1);
    glutSwapBuffers(); // Required to copy color buffer onto the screen.

}


void display() {  // Display function will draw the image.
 
    glClearColor( 0, 0, 0, 0 );  // (In fact, this is the default.)
    glClear( GL_COLOR_BUFFER_BIT );
    glBegin(GL_TRIANGLES);
    glColor3f( 1, 0, 0 ); // red
    glVertex2f( -0.8, -0.9 );
    glColor3f( 1, 0, 0 ); // green
    glVertex2f( 0.8, -0.9 );
    glColor3f( 1, 0, 0 ); // blue
    glVertex2f( 0, 0.9 );
    glEnd(); 
    glutSwapBuffers();
    draww(x1,x2,x3,y1,y2,y3,5);
}



int main( int argc, char** argv ) {  // Initialize GLUT and 

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE);    // Use single color buffer and no depth buffer.
    glutInitWindowSize(600,600);         // Size of display area, in pixels.
    glutInitWindowPosition(100,100);     // Location of window in screen coordinates.
    glutCreateWindow("GL RGB Triangle"); // Parameter is window title.
    glutDisplayFunc(display);            // Called when the window needs to be redrawn.
    
    glutMainLoop(); // Run the event loop!  This function does not return.
                    // Program ends when user closes the window.
    return 0;

}

