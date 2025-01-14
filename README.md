# TB-POV-RAY

![](./.github/showoff.png)

A basic toolchain for creating [POV-Ray](http://www.povray.org) scenes in
[TrenchBroom](https://trenchbroom.github.io/).

Huge thanks to [.:/ DiSCATTe \\:.](https://discatte.github.io/) and
[Spoike](https://triptohell.info/) for helping me figure out the best ways to
translate the map data to POV-Ray. This wouldn't have been possible without
them!

## Usage

1. Copy the [`POV-Ray`](/POV-Ray/) folder to your TrenchBroom games directory.
2. Setup the game configuration to point to the appropriate tools (`tb2pov.py`
and `povray`).
3. Build a map.
4. Use the TrenchBroom "Compile" dialog to automatically export and render the
scene!

## Notes

- Textures must be in PNG format.
- Textures must be copied to the `scenes` folder for POV-Ray to find them.

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

