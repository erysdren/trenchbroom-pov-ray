# TB-POV-RAY

![](./.github/showoff.png)

A basic toolchain for creating [POV-Ray](http://www.povray.org) scenes in
[TrenchBroom](https://trenchbroom.github.io/).

Huge thanks to [.:/ DiSCATTe \\:.](https://discatte.github.io/) and
[Spoike](https://triptohell.info/) for helping me figure out the best ways to
translate the map data to POV-Ray. This wouldn't have been possible without
them!

## Installation

1. Clone or download the whole repository
2. Copy the [`POV-Ray`](/POV-Ray/) folder to your TrenchBroom games directory.
3. Setup the game configuration to point to the this repository as the Game
Path.
4. Setup the game configuration to point to the appropriate tools (`tb2pov.py`
and `povray`).
5. Build a map.
6. Use the TrenchBroom "Compile" dialog to automatically export and render the
scene!

## Materials

POV-Ray materials can be used, but must also exist in PNG format for
TrenchBroom to use them. The compiler will look for `{texturename}.inc` to
find a text file with the POV-Ray material in it. For example,
`textures/Polished_Chrome.inc` could contain:

```
#declare Polished_Chrome =
texture {
    pigment { rgb <0.2, 0.2, 0.2> }
    finish {
        ambient 0.1
        diffuse 0.7
        brilliance 6.0
        reflection 0.6
        phong 0.8
        phong_size 120
    }
}
```

or it could contain:

```
#include "textures.inc"
```

both will work in this case.

## Notes

- Textures *must* be in PNG format.

## License

MIT License

Copyright (c) 2025 erysdren (it/its)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

