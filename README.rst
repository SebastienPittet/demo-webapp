demo-webapp
===========

|Build Status|

This application is written in Python and based on
`Flask <https://flask.palletsprojects.com/>`__. The template uses
`Bootstrap framework <https://getbootstrap.com/>`__. It only show some
content for **demo purpose**.

In its initial release, it is mainly a wrapper of a
Single-page-Application (SPA) stored on Exoscale `Simple Object Storage
(SOS) <https://www.exoscale.com/object-storage/>`__ but can evolve
differently in the future.

From the release of August 1st, it fetch a random advice from
`adviceslip.com Open API <https://api.adviceslip.com/>`__.

October, 1st: added /slow to prepare some horizontal autoscaling demos.

.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/SebastienPittet/demo-webapp.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/SebastienPittet/demo-webapp/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/SebastienPittet/demo-webapp.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/SebastienPittet/demo-webapp/context:python
.. |Build Status| image:: https://app.travis-ci.com/SebastienPittet/demo-webapp.svg?branch=master
    :target: https://app.travis-ci.com/SebastienPittet/demo-webapp
