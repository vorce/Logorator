import unittest
from hamcrest import *
from generators import polygen


class WebGL(object):
    def convert_to_threejs(self, vertices, draw_mode):
        threejs_header = """
var Shape = function () {

    var scope = this;
    THREE.Geometry.call(this);
"""
        threejs_vertices = ""
        vertice_pairs = self._get_vertice_pairs(vertices)
        for vertice in vertice_pairs:
            threejs_vertices += "    v({0}, {1}, 0.0);\n".format(vertice[0], vertice[1])
            
        threejs_faces = ""
        for face in range(len(vertice_pairs) - 2):
            threejs_faces += "    f({0}, {1}, {2});\n".format(0, face + 1, face + 2)
        
        threejs_footer = """    function v(x, y, z) {
        scope.vertices.push(new THREE.Vector3(x, y, z));
    }
    
    function f(x, y, z) {
        scope.faces.push(new THREE.Face3(x, y, z))
    }
}

Shape.prototype = new THREE.Geometry();
Shape.prototype.constructor = Shape;
"""
        
        return "{0}\n{1}\n{2}\n{3}".format(threejs_header, threejs_vertices,
                                           threejs_faces, threejs_footer)


    def _get_vertice_pairs(self, vertices):
        pairs = []
        
        i = 0
        while i < (len(vertices) - 1):
            pairs.append((vertices[i], vertices[i + 1]))
            i += 2
        
        return pairs

class WebGLTest(unittest.TestCase):
    def test_get_vertice_pairs(self):
        poly_gen = polygen.PolyGen()
        triangle = poly_gen.ngon(0, 0, 10, 3)
        wgl = WebGL()
        
        vertice_pairs = wgl._get_vertice_pairs(triangle)

        assert_that(len(vertice_pairs), is_(len(triangle) / 2 ))
        
    def test_polygen_web_gl_output_can_be_read_by_threejs(self):
        poly_gen = polygen.PolyGen()
        triangle = poly_gen.ngon(0, 0, 10, 4)
        wgl = WebGL()
        threejs_output = wgl.convert_to_threejs(triangle)
        print threejs_output