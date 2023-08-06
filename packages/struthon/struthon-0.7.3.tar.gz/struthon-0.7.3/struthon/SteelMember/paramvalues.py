'''
--------------------------------------------------------------------------
Copyright (C) 2015-2020 Lukasz Laba <lukaszlaba@gmail.com>

This file is part of Struthon.
Struthon free open source structural engineering design python applications.

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Struthon; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------

File changes:
- python3 compatibility checked
'''

wlim_ratio =    {
                    '1/100' :   0.01,
                    '1/150' :   0.0066,
                    '1/200' :   0.005,
                    '1/250' :   0.004,
                    '1/300' :   0.0033,
                    '1/500' :   0.002,
                }

alpha_k =       {
                    'simply supported with mid point force - 1/12'  :   0.0833,
                    'simply supported with uniform load - 5/48'     :   0.1042,
                    'cantilever with end point force - 1/3'         :   0.3333,
                    'cantilever with uniform load - 1/4'            :   0.2500,
                    'None - 0'                                      :   0.0000,
                }


#Test if main
if __name__ == "__main__":
    print(wlim_ratio)
    print(wlim_ratio.keys())
    print(alpha_k)
    print(alpha_k.keys())