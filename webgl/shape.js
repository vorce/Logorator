var ThreeObject = function() {
var Shape = function () {
    var scope = this;
    THREE.Geometry.call(this);
        
    v(10.0, 0.0, 0.0);
    v(6.12323399574e-16, 10.0, 0.0);
    v(-10.0, 1.22464679915e-15, 0.0);
    v(-1.83697019872e-15, -10.0, 0.0);
    v(10.0, -2.44929359829e-15, 0.0);

    f(0, 1, 2);
    f(0, 2, 3);
    f(0, 3, 4);

    function v( x, y, z ) {
        scope.vertices.push(new THREE.Vector3(x, y, z));
    }
    
    function f(x, y, z) {
        scope.faces.push(new THREE.Face3(x, y, z))
    }
}

Shape.prototype = new THREE.Geometry();
Shape.prototype.constructor = Shape;
return new THREE.Mesh(new Shape(),
                          new THREE.MeshBasicMaterial( { color: 0xffaa00, wireframe: false, side: THREE.DoubleSide } ))

}
