## Qwen Added Memories
- JSCAD v2 Scripting Rules for this project:
1. Signature: `const main = (params = {}) => { ... };` — always this exact form
2. NO imports: Never use `import`, `require()`, or `from`. All APIs are injected into scope
3. NO side effects: Pure function only — no `console.log`, no `Deno.*`, no `fetch`
4. MUST return geometry: Return a single geometry or array of geometries
5. Namespace access: Use `primitives.cuboid()`, `booleans.subtract()`, `transforms.translate()` etc. — never bare names
6. Size as array: `cuboid({ size: [x,y,z] })` — never `size: 10`
7. Center as array: `center: [x,y,z]` — never `center: true`
8. Cylinder: `{ radius: 5, height: 20 }` — never `r`, `h`, or `length`
9. Radians: `rotate([rx, ry, rz], shape)` — values in radians, not degrees
10. Oversized cutters: When using `subtract()` for holes/cavities, cutter must be taller than outer body + 2mm to prevent z-fighting
11. Named Coordinates: Every position and dimension must be a named constant. NO inline arithmetic in `center:` or `translate()`
12. Feature-Based Modeling: Establish datums (Z=0 base, axis of symmetry), decompose into features, use ratios for dimensions
13. Handles: Use `hulls.hull()` or `hulls.hullChain()` of spheres/cylinders — NOT `torus()`
14. Symmetric bodies: Use `extrudeLinear`, `extrudeRotate` with `segments: 64`

Injected Scope (available without import):
- primitives: cuboid, roundedCuboid, cylinder, sphere, torus, cone, polygon, circle, square
- transforms: translate, rotate, scale, mirror, align, center
- booleans: subtract, union, intersect
- extrusions: extrudeLinear, extrudeRotate, extrudeFromSlices
- hulls: hull, hullChain
- measurements: measureBoundingBox, measureVolume, measureSurfaceArea
- colors: colorize, colorNameToRgb

Project paths: /Users/user/jscad/test/
