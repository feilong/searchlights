:py:mod:`searchlights`
======================

.. py:module:: searchlights

.. autoapi-nested-parse::

   
















   ..
       !! processed by numpydoc !!


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   searchlights.get_mask
   searchlights.get_searchlights



.. py:function:: get_mask(lr, mask_space='fsaverage', icoorder=None)

   
   Get the boolean cortical mask.


   :Parameters:

       **lr** : {'l', 'r'}
           Get the mask for the left ('l') or right ('r') hemisphere.

       **mask_space** : {'fsaverage', 'fsaverage6', 'fsaverage5', 'none'}, optional
           Which cortical mask to get. Note that the masks slightly differ
           for different ``mask_space``, even at the same resolution.

       **icoorder** : int or None
           The spatial resolution of the output mask. If it's an integer, the
           resolution of the output mask will be reduced so that it won't be
           higher than the desired ``icoorder``. If it's None, then the
           resolution will not be reduced.

   :Returns:

       **mask** : ndarray
           A boolean array. The value is True for cortical vertices and False
           for non-cortical vertices. The resolution is determined by
           ``icoorder``.













   ..
       !! processed by numpydoc !!

.. py:function:: get_searchlights(lr, radius, mask_space='fsaverage', icoorder=5, return_distances=False)

   
   Get searchlight indices based on precomputed files.


   :Parameters:

       **lr** : {'l', 'r'}
           Get the searchlights for the left ('l') or right ('r') hemisphere.

       **radius** : int or float
           The searchlight radius.

       **mask_space** : {'fsaverage', 'fsaverage6', 'fsaverage5', 'none'}, optional
           Which cortical mask to be used for the searchlights. The mask
           should be the same as the one applied to brain data matrices.

       **icoorder** : int, default=5
           The spatial resolution of cortical vertices. This should also be
           the same as that of your data matrices.

       **return_distances** : bool, default=False
           Whether to also return the distances to the searchlight center
           (True) or not (False). If ``return_distances=True``, two lists are
           returned instead of one.

   :Returns:

       **sls** : list of ndarray
           Each entry is an ndarray of integers, which are the indices of the
           vertices in a searchlight.

       **dists** : list of ndarray
           Each entry is an ndarray of float numbers, which are the distances
           between vertices in a searchlight and the center of the
           searchlight. The order of vertices are the same as ``sls``. Only
           returned when ``return_distances=True``.













   ..
       !! processed by numpydoc !!

