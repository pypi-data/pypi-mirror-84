<p align="center">
  <img src="https://raw.githubusercontent.com/diegohdorta/models/master/media/pyeiq.png" height="191" width="176">
</p>

##  **A Python Demo Framework for eIQ on i.MX Processors**

![pip3][eiqpackage]
[![PyPI version](https://badge.fury.io/py/eiq.svg)](https://badge.fury.io/py/eiq)
![GitHub issues][license]
[![Downloads](https://pepy.tech/badge/eiq)](pepy_total)
[![Downloads](https://pepy.tech/badge/eiq/month)](pepy_month)
[![Downloads](https://pepy.tech/badge/eiq/week)](pepy_week)
![Total Lines][total_lines]
![Repo Size][repo_size]
![Closed Issues][closed_issues]
![Open Issues][open_issues]
[![Gitter][gitter-image]][gitter-url]

PyeIQ is written on top of [eIQ™ ML Software Development Environment][eiq] and
provides a set of Python classes allowing the user to run Machine Learning
applications in a simplified and efficiently way without spending time on
cross-compilations, deployments or reading extensive guides.

* **Take as a disclaimer that PyeIQ should not be considered production-ready**.
* Go to the documentation page for further details [pyeiq.dev][page].

### Official Releases

| BSP Release                  | PyeIQ Release       | PyeIQ Updates    | Board          | Date      | Status             | Notes   |
|------------------------------|---------------------|------------------|----------------|-----------|--------------------|---------|
| ![BSP][release_5.4.3_2.0.0]  | ![tag][tag_v100]    |                  | ![imx][boards] | Apr, 2020 | ![Build][passing]  | PoC     |
|                              |                     | ![tag][tag_v101] | ![imx][boards] | May, 2020 | ![Build][passing]  |         |
| ![BSP][release_5.4.24_2.1.0] | ![tag][tag_v200]    |                  | ![imx][boards] | Jun, 2020 | ![Build][passing]  | Stable  |
|                              |                     | ![tag][tag_v201] | ![imx][boards] | Jun, 2020 | ![Build][passing]  |         |
|                              |                     | ![tag][tag_v210] | ![imx][boards] | Aug, 2020 | ![Build][passing]  |         |
| ![BSP][release_5.4.47_2.2.0] |                     | ![tag][tag_v220] | ![imx][boards] | Nov, 2020 | ![Build][passing]  |         |

![blue][tag_blue]
![yellow][tag_yellow]
![red][tag_red]

### Major Changes

**2.0.0**
- General major changes on project structure.
- Split project into engine, modules, helpers, utils and apps.
- Add base class to use on all demos avoiding repeated code.
- Support for more demos and applications including Arm NN.
- Support for building using Docker.
- Support for download data from multiple servers.
- Support for searching devices and build pipelines.
- Support for appsink/appsrc for QM (not working on MPlus).
- Support for camera and H.264 video.
- Support for Full HD, HD and VGA resolutions.
- Support video and image for all demos.
- Add display info in the frame, such as: FPS, model and inference time.
- Add manager tool to launch demos and applications.
- Add document page for PyeIQ project.

**1.0.0**
- Support demos based on TensorFlow Lite (2.1.0) and image classification.      
- Support inference running on GPU/NPU and CPU.
- Support file and camera as input data.
- Support SSD (Single Shot Detection).
- Support downloads on the fly (models, labels, dataset, etc).
- Support old eIQ demos from eiq_sample_apps CAF repository.
- Support model training for host PC.
- Support UI for switching inference between GPU/NPU/CPU on TensorFlow Lite.

### Copyright and License

Copyright 2020 NXP Semiconductors. Free use of this software is granted under
the terms of the BSD 3-Clause License.
See [LICENSE](https://github.com/diegohdorta/pyeiq/blob/master/LICENSE.md)
for details.

[release_5.4.3_2.0.0]: https://img.shields.io/badge/-5.4.3__2.0.0-blueviolet
[release_5.4.24_2.1.0]: https://img.shields.io/badge/-5.4.24__2.1.0-blueviolet
[release_5.4.47_2.2.0]: https://img.shields.io/badge/-5.4.47__2.2.0-blueviolet

[tag_blue]: https://img.shields.io/badge/-new-blue
[tag_yellow]: https://img.shields.io/badge/-features-yellow
[tag_red]: https://img.shields.io/badge/-bug%20fixes-red

[tag_v100]: https://img.shields.io/badge/-v1.0.0-blue
[tag_v101]: https://img.shields.io/badge/-v1.0.1-red
[tag_v110]: https://img.shields.io/badge/-v1.1.0-red

[tag_v200]: https://img.shields.io/badge/-v2.0.0-blue
[tag_v201]: https://img.shields.io/badge/-v2.0.1-red
[tag_v210]: https://img.shields.io/badge/-v2.1.0-yellow
[tag_v220]: https://img.shields.io/badge/-v2.2.0-red

[boards]: https://img.shields.io/badge/-8QM%2C%208MPlus-lightgrey
[passing]: https://img.shields.io/badge/Build-passing-success

[page]: https://pyeiq.dev/
[eiq]: https://www.nxp.com/design/software/development-software/eiq-ml-development-environment:EIQ
[eiqpackage]: https://img.shields.io/badge/pip3%20install-eiq-green
[pypirepo]: https://pypi.org/project/eiq/#description
[pypicaf]: https://source.codeaurora.org/external/imxsupport/pyeiq/
[license]: https://img.shields.io/badge/License-BSD%203--Clause-blue
[pepy_total]: https://pepy.tech/project/eiq
[pepy_month]: https://pepy.tech/project/eiq/month
[pepy_week]: https://pepy.tech/project/eiq/week
[gitter-url]: https://gitter.im/pyeiq-imx/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
[gitter-image]: https://badges.gitter.im/pyeiq-imx/community.svg


[total_lines]: https://img.shields.io/tokei/lines/github/diegohdorta/pyeiq
[repo_size]: https://img.shields.io/github/repo-size/diegohdorta/pyeiq
[closed_issues]: https://img.shields.io/github/issues-closed-raw/diegohdorta/pyeiq
[open_issues]: https://img.shields.io/github/issues-raw/diegohdorta/pyeiq
