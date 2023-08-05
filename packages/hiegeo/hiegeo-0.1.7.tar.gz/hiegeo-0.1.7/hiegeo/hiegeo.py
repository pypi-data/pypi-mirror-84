"""
:License:
    This file is part of hiegeo.

    hiegeo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    hiegeo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with hiegeo.  If not, see <https://www.gnu.org/licenses/>.

:This file:

    ``hiegeo.py``

:Purpose:

    hie-geo: "hierarchical geo-modeling"

    A module containing the functions required to read information
    from a geological data-set (contact point) and plot in a
    hierarchical fashion the unit sections.

:Usage:
    See ``hiegeo_test-simple.py`` and ``hiegeo_test-full.py`` for an example usage.

:Version:
    1.9.1, 2020-03-11 :
        - Improved the colorscale (color blindness OK)
        - Improved the provided dataset (smooth topography)
        - Improved the overlapping order of the different topographies
        - Added borders to line representation in order to provide more
          flexibility for the usage of different colorscales.
    1.9, 2019-10-02 :
        Some clean up an adding License information.
    1.8, 2019-07-31 :
        Version updated with some clean up, before important changes in "rank" 
        and "order" definitions...

:Some conventions:
    SB:
        Stratigraphic Bound
    SU:
        Stratigraphic Unit
    Hierarchy:
        Minumum value stands for lower hierarchical importance;  higher
        values are for more important SBs.
    chronology:
        This is the temporal order of the SBs. Lower values corresponds to older
        SBs, while higher values correspond to more recent SBs.

:Authors:
    Alessandro Comunian

:License:
    `hiegeo` is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    `hiegeo` is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with `hiegeo`.  If not, see <https://www.gnu.org/licenses/>.

.. note::
    1) At the moment, the points of intersection among surfaces are a
       required input data. Also, it is expected that when two SBs are
       intersecting at one point, the point is defined in the dataset
       for both the SBs.

"""


import numpy as np
import matplotlib.pylab as pl
import gc
import warnings
import anytree as at
import sys
import matplotlib.patheffects as pe

# This is to avoid warning with the broken_line function
warnings.simplefilter('ignore', np.RankWarning)


class SBound(at.NodeMixin):
    """
    A class useful to contain all the properties of a Stratigraphic
    Boundary (SB).
    """

    def __init__(self, name, data=None, hierarchy=None, chronology=None,
                 xd=None, color=None, parent=None):
        """
        Arguments:
            name: string
                Name of the SB
            data: DataFrame
                If provided, this argument contains the data contained
                in the contact points CSV file. See the documentation for more
                details about this data format.
            hierarchy: integer
                The hierarchy of the SB. See `notes` for more details.
            chronology: integer
                The chronology (temporal) of the SB. See `notes` for more
                details.
            xd: numpy array
                The discretized coordinates where to compute the corresponding
                `zd`.
            color: a color code according to matplotlib standards.
                The color to be used when plotting the SB.
                (see the JSON input file for an example).
            parent: SBound object
                This is the "parent" SB, in the upper hierarchical level, useful
                to define a hierarchy.

        .. warning::
            If the argument `data` is provided, then the other arguments 
            `hierarchy` and `chronology` are extracted directly from the data
            and the provided values as arguments are ignored!

        .. note:: 
            To allow the recongnition of intersections, when added manually,
            you should first add all the SBs of the highest hierarchy, and then
            add the other SB with a decreasing hierarchy chronology.

        Example:
            To create a SB "manually", you can simply:
  
            S0sb = hiegeo.SBound(name="S0", data=data, xd=x,
                                 color=par["colors"]["S0"])

        """

        # Set the name of the SB
        self.name = name

        if data is not None:
            # Data with correlation/contact point definitions is provided

            # Collect all the points whith the selected "name"
            data_loc = data[data["sb_name"] == name].sort_values(by=["x"])
            self.hierarchy = get_sb_hierarchy(data, self.name)
            self.chronology = get_sb_chronology(data, self.name)            
            # (better to do a copy to avoid some overwriting problems...)
            self.raw_coord = data_loc[["x", "z"]].copy()

            # Check if the current SB intersects some other SB
            inters = get_intersect(self.name, data)
            
            if not inters.empty:
                print("")
                # There is at least one intersection
                print('    SB "{0}" intersects with:'.format(self.name))
                # In principle, if I instantiate all the SBs with the
                # provided function `create_sb_from_data`, everithing is made
                # in the right order and there is no need to add any recursive
                # check here...
                for index, inter in inters.iterrows():
                    inter_name = inter["sb_name"]
                    inter_x = inter["x"]
                    print('        - {0}, point({1},{2})'.format(inter_name,
                          inter["x"], inter["z"]))
                    if self.hierarchy < get_sb_hierarchy(data, inter_name):
                        # SB can be cut only by hierarchies >=
                        
                        # In this case there is the possibility that a SB of
                        # greater hierarchy can be used as "continuation" for
                        # the current SB.

                        if self.chronology > get_sb_chronology(data, inter_name):

                            # Check if the continuation should be on the left
                            # or on the right

                            # WARNING: This may not work if the SBs
                            # are defined as many separated segments.
                            x_min = self.raw_coord["x"].min()
                            x_max = self.raw_coord["x"].max()               
                            # The intersection line should be added to the SB

                            if inter_x == x_min:
                                # we are on the left
                                cont_sx = data[(data["sb_name"]==inter_name) &
                                               (data["x"] < inter_x)]
                                if not cont_sx.empty:
                                    print("              added {0} points to the left".format(len(cont_sx)))
                                    self.raw_coord = self.raw_coord.append(cont_sx[["x", "z"]])
                            elif inter_x == x_max:
                                # we are on the right
                                cont_dx = data[(data["sb_name"]==inter_name) &
                                               (data["x"] > inter_x)]
                                if not cont_dx.empty:
                                    print("              added {0} points to the right".format(len(cont_dx)))
                                    self.raw_coord = self.raw_coord.append(cont_dx[["x", "z"]])
                            else:
                                print("")
                                print("    WARNING: the coordinate *x* of the intersection")
                                print("        should be the min or the max of  the main SB,")
                                print("        double check (for example, check the chronology of the SB)!")
                                print("")
            else:
                # In this case there is no intersection
                print('    SB "{0}": no intersections'.format(self.name))

            if xd is not None:
                # Interpolate the SB as a broken line
                self.xd = xd
                self.broken_line()

            if hierarchy is not None:
                print("    WARNING: argument 'hierarchy' of 'SBound' ignored!")
                print("        (when the argument 'data' is provided,")
                print("        then the hierarchy is extracted from there...)")
            if chronology is not None:
                print("    WARNING: argument 'chronology' of SBound ignored!")
                print("        (when the argument 'data' is provided,")
                print("        then the chronology is extracted from there...)")
            if parent is not None:
                # If parent is provided, assign it
                self.parent = parent
        else:
            # No "data" argument provided
            self.chronology = chronology
            self.hierarchy = hierarchy
            self.xd = xd

        # Set the color (plotting purposes only)
        self.color = color

    def broken_line(self):
        """
        This is useful to create, for each point of the provided discretization
        along *x* axis, (`self.xd`), a broken line. A `numpy.nan` value is set
        where the provided "raw" coordinates does not allow to complete the 
        discretization.
        """
        # This is the list of "conditions"
        cl = []
        # This is the list of "functions"
        fl = []

        # Collect the coordinates of the well_id/virtual points

        # Here I sort to prevent that added continuation values would
        # alter somehow the calculations...
        x0 = np.asarray(self.raw_coord.sort_values(by=["x"])["x"])
        z0 = np.asarray(self.raw_coord.sort_values(by=["x"])["z"])        

        cl.append(self.xd < x0[0])
        fl.append(np.nan)
        for i in range(len(x0)-1):
            ab = np.polyfit(x0[i:i+2], z0[i:i+2], 1)
            # Compute and append a "condition" interval
            cl.append(np.logical_and(self.xd >= x0[i], self.xd <= x0[i+1]))
            # Create a line function for the interval
            fl.append(lambda x_in, ab=ab: x_in*ab[0] + ab[1])
        cl.append(self.xd > x0[-1])
        fl.append(np.nan)
        self.zd = np.piecewise(self.xd, condlist=cl, funclist=fl)

    def __str__(self, hie=False):
        """
        Print out some info about a SB.

        .. note: The parameter `hie` is still there for future development.
        """
        out = ""
        out = ('\n    SBound "{0}"\n'
               "    - hierarchy: {1}\n"
               "    - chronology: {2}\n"
               #"    - x_raw(size): {3}\n"
               #"    - z_raw(size): {4}"
               .format(self.name,
                       self.hierarchy,
                       self.chronology,
               )
        )
        return(out)

    def print_hie(self):
        """
        Print out some info about a SB, in a hierarchical fashion.
        """
        out = ""
        for pre, _, node in at.RenderTree(self):
            # Only the SB name is printed
            treestr = "  {0}{1}\n".format(pre, node.name)
            out += treestr
        return(out)
    
    def plot(self, lw=None, chronology=None):
        """
        Plot the SB.

        Parameters:
            lw: integer
                This is the line width
            chronology: integer
                The relative chronology of the SB.

        .. note::
            The values where ``zd==np.nan`` are not plotted.
        """
        pl.plot(self.xd, self.zd, label="{0} ({1})".format(self.name,
                self.chronology), linewidth=lw)        


    def plot_ax(self, ax, lw=None, color=None):
        """
        Plot the SB when a matplotlib axis is provided.
        
        Parameters:
            lw: integer (optional)
                The line width. Using directly the hierarchies (for example,
                with hierarchies from 1 to 3) seems to provide a figure which
                is OK
            color: color code (optional)
                The line color.
            
        .. note::
            The values where `zd==np.nan` are not plotted.

        """
        try:
            ax.plot(self.xd, self.zd, label="{0} ({1})".format(self.name,
                                                               self.chronology), linewidth=lw, color=self.color,
                    path_effects=[pe.Stroke(linewidth=lw+0.5,
                                            foreground='black'),
                                  pe.Normal()])
        except:
            x = self.raw_coord.sort_values(by=["x"])["x"]
            z = self.raw_coord.sort_values(by=["x"])["z"]            
            ax.plot(x, z, label="{0} ({1})".format(self.name, self.chronology),
                    linewidth=lw, color=self.color,
                    path_effects=[pe.Stroke(linewidth=lw+0.5,
                                            foreground='black'),
                                  pe.Normal()])

    def get_ancestors(self, anc_list=[]):
        """
        Provide a list of ancestors of the current SB.

        Parameters:
            anc_list: list
                A partially filled input list can be provided, to
                allow appending additional ancestors.
        """
        if self.parent.parent == None:
            exit
        else:
            anc_list.append(self.parent)
            print("working on", self.name)
            self.parent.get_ancestors(anc_list)            
        return(anc_list)

    def get_obj_above(self, hierarchy):
        """
        Get all the SBs defined in the script with the given hierarchy,
        ordeder by "chronology".
        
        Parameters:
            hierarchy: integer
                The hierarchy of the SBs to be plotted.
        Returns:
            A list containing all the defined SBs with the given hierarchy, 
            ordered by "chronology".
        
        """
        # Collect all the objects defined in the calling script
        all_obj = gc.get_objects()
        
        sb_obj = []

        for obj in all_obj:
            if type(obj) is SBound:
                if ((obj.chronology > self.chronology) and
                    (obj.hierarchy >= hierarchy)):
                    sb_obj.append(obj)
                    
        return(sorted(sb_obj, key=lambda sb: sb.chronology))

    def plot_fill(self, ax, hierarchy, alpha):
        """
        "fill_between" plot of a SU given the bottom SB.

        Parameters:
            ax: matplotlib axis
                The object where to make the plot
            hierarchy: integer
                Hierarchy.
            alpha: float
                Transparency level.

        .. note::
            Using `alpha` as parameter could create problems when one 
            tries to properly represent overlapping regions.
            (and this, in principle, should happen quite frequently when
            dealing with hierarchical models...)
        """
        ax.fill_between(self.xd,
                        self.zd,
                        get_allmin(self.get_obj_above(hierarchy)),
                        where=~np.isnan(self.zd),
                        label=self.name,
                        facecolor=self.color,
                        alpha = alpha,
                        edgecolor="black", lw=0.5
        )

        
class SUnit(object):
    """
    A class useful to contain all the properties related to a SU.

    .. note::
        Is is expected that in the same script all the SBounds were already 
        created extracting the information from the correlation/contact points file.
    .. warning::
        The development of this Class is still work in progress, and only
        basic functionalities are provided for the moment.
    """

    def __init__(self, name=None, bot=None, top=None, sbs=None, id=None):
        """
        Arguments:
            name: string
                The SU takes its name from the SB that defined its bottom.
                Alternatively, one can define explicitly its name.
            bot: SBound
                This is(are) the SB(s) that defines the bottom of the SU
            top: SBound
                This is(are) the SB(s) that defines the top of the SU
            sbs: list of all the stratigraphyc bounds
            id: string
                Under development.

        """
        if name is not None:
            self.name = name
        else:
            self.name = bot.name

        if bot is not None:
            self.bot = bot #[]
#        else:
#            self.bot = get_bot_sb(bot, sbs)
            
        if top is not None:
            self.top = top
        else:
            self.top = get_top_sb(bot, sbs)

        if id is not None:
            self.id = id

        # Compute the *z* of the top/bottom
        zd_top = [sb.zd for sb in self.top]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.z_top = np.nanmin(np.stack(zd_top), axis=0)
        self.z_bot = bot.zd

        # Restrict the domain of the SU depending of the intersections
        # with more recent SBs.
        self.domain = np.logical_not(np.isnan(self.z_bot))
        
    def __str__(self):
        """
        Print out some info about the SU.
        """
        out = ""
        out = ('\n    SUnit "{0}"\n'
               '    *** bottom *** {1}'
               '    *** top ***\n'
               '    {2}\n'
               .format(
                   self.name,
                   self.bot,
                   [obj.name for obj in self.top],
               )
        )
        return(out)

    def plot(self):
        """
        Plot a SU
        """
        pl.fill_between(self.top[0].xd, self.z_bot, self.z_top,
                        where=self.domain, label=self.name)
        

def get_unique_sb_name(data):
    """
    Get an ordered list containing the unique names of the 
    SBs.

    Parameters:
        data: input DataFrame
            See the documentation for more details about the data format.
    Returns:
        A list containing the ordered ids
    """
    return(data[data["sb_name"].notnull()].sort_values(
        by=["x", "z"])["sb_name"].drop_duplicates().tolist())

def get_sb_hierarchy(data, sb):
    """
    Get the hierarchy of the current SB.

    Parameters:
        data: DataFrame
            The point correlation info contained in the DBF file
        sb: string
            Name of the SB.

    .. warning:
        Wrong definition in the file could cause a corrupted output.
    """
    return(data[data["sb_name"] == sb]["hierarchy"].drop_duplicates().tolist()[0])

def get_sb_chronology(data, sb):
    """
    Get the chronology of the current SB.

    Parameters:
        data: DataFrame
            The point correlation info contained in the DBF file
        sb: string
            Name of the SB.

    .. warning:
        Wrong definition in the file could cause a corrupted output.

    """
    return(data[data["sb_name"] == sb]["chronology"].drop_duplicates().tolist()[0])

def create_sb_by_hierarchy(data, hierarchy, xd, color=None):
    """
    Given a data set containing the correlation points and a hierarchy,
    create a list of SB objects.

    Parameters:
        data: DataFrame
            The info about the correlation points
        hierarchy: integer
            The hierarchy that should be created
        xd: numpy array
            Discretized *x* coordinate
    Returns:
        A list containing the SB objects, ordered by "chronology"
    """

    data_sel = data[data["hierarchy"] == hierarchy].sort_values(
            by=["chronology"])["sb_name"].drop_duplicates()

    sb_list = []

    for datum in data_sel:
        # Loop on all the SB of the current hierarchy
        sb_parent_name = get_parent_by_name(data, datum)
        sb_parent_obj = get_sbobj_by_name(sb_parent_name)
        if sb_parent_obj is not None:
            # Hierarchy is < highest hierarchy, 
            sb_list.append(SBound(datum, data, xd=xd, parent=sb_parent_obj,
                                  color=sb_parent_obj.root.color))
        else:
            # In this case no parent SB is found.
            try:
                sb_list.append(SBound(datum, data, xd=xd, parent=None,
                                      color=color[datum]))
            except KeyError:
                err_msg = ("    ERROR: inconsistency between hierarchy or missing data.\n"
                           "               - hierarchy of the current SB: {0}\n"
                           "               - name of the current SB: {1}\n"
                           "           Double check:\n"
                           "               1) Hierarchy/chronology of the current SB.\n"
                           "               2) Was a color provided in the JSON parameter file?").format(hierarchy, datum)
                sys.exit(err_msg)
        
    return(sb_list)

def get_max_chronology(data):
    """
    Get the maximum chronology defined in the dataset.

    Parameters:
        data: DataFrame
            Info about the correlation points
    Return:
        The value of the max chronology
    """
    return(data["chronology"].max())


def get_unique_hierarchy(data):
    """
    Extract from a dataset al the defined hierarchies.

    Parameters:
        data: DataFrame
            Info about the correlation points
    Return:
        A list containing the defined hierarchies.
    """
    return(sorted(data["hierarchy"].drop_duplicates().tolist(), reverse=True))

def get_unique_chronology(data):
    """
    Extract from a dataset al the defined chronologies.

    Parameters:
        data: DataFrame
            Info about the correlation points
    Return:
        A list containing the defined chronologies.
    """
    return(sorted(data["chronology"].drop_duplicates().tolist()))

    
def create_sb_from_data(data, xd, color=None):
    """
    Create all the SBs defined in a dataset

    Parameters:
        data: DataFrame
            Info about the correlation points
    Returns:
        A dictionary containing, for each hierarchy, a list
        of SBs.
    """
    unique_hie = get_unique_hierarchy(data)
    

    sb_dict = {}
    for hie in unique_hie:
        sb_dict[hie] = create_sb_by_hierarchy(data, hie, xd, color=color)
    return(sb_dict)

def get_sbobj_by_hie(hierarchy, mode="eq", reverse=False):
    """
    Get all the SBs defined in the script with the given hierarchy,
    ordeder by "chronology".

    Parameters:
        hierarchy: integer
            The hierarchy of the SBs to be plotted.
        mode: in ("eq" or "ge")
            Depending on this optional value, one can get all the SBs
            of the same hierarchy (mode="eq") or all the objects with
            a >= hierarchy.
    Returns:
        A list containing all the defined SBs with the given hierarchy, 
        ordered by "chronology".

    """
    # Collect all the objects defined in the calling script
    all_obj = gc.get_objects()

    sb_obj = []

    for obj in all_obj:
        if type(obj) is SBound:
            try:
                if mode == "eq":
                    if obj.hierarchy == hierarchy:
                        sb_obj.append(obj)
                elif mode == "ge":
                    if obj.hierarchy >= hierarchy:
                        sb_obj.append(obj)
                else:
                    print('        WARNING: wrong mode in function "get_sbobj_by_hie"')
            except AttributeError:
                print('    WARNING: no defined hierarchy for a SBound object.')
            
    return(sorted(sb_obj, key=lambda sb: sb.chronology, reverse=reverse))

def get_sbobj():
    """
    Get all the SBs defined within the script,
    ordeder by "chronology".

    Returns:
        A list containing all the defined SBs ordered by "chronology".

    """
    # Collect all the objects defined in the calling script
    all_obj = gc.get_objects()

    sb_obj = []

    for obj in all_obj:
        if type(obj) is SBound:
            sb_obj.append(obj)
    return(sorted(sb_obj, key=lambda sb: sb.chronology))

def get_sbobj_by_name(sb_name):
    """
    Get all the SBs defined within the script,
    ordeder by "chronology".

    Returns:
        A list containing all the defined SBs ordered by "chronology".

    """
    # Collect all the objects defined in the calling script
    all_obj = gc.get_objects()

    for obj in all_obj:
        if type(obj) is SBound:
            if obj.name == sb_name:
                return obj



def plot_sb_by_hie(hierarchy):
    """
    Plot all the SB of a given hierarchy.

    Parameters:
        hierarchy: integer
            The hierarchy of the SBs to be plotted
    """
    sbs = get_sbobj_by_hie(hierarchy)

    for sb in sbs:
        sb.plot(lw=hierarchy)

def plot_sb_by_hie_ax(ax, hierarchy, palette=None):
    """
    Plot all the SB of a given hierarchy.

    Parameters:
        ax: axis object
            The axis object where the plot should be made
        hierarchy: integer
            The hierarchy of the SBs to be plotted
        palette: dictionary
            A dictionary containing the correspondence between
            SB name and plotting color.
    """
    # Collect all the defined objects of a given hierarchy
    sbs = get_sbobj_by_hie(hierarchy)

    for sb in sbs:
        sb.plot_ax(ax, lw=hierarchy)
    return(ax)        
        

# def plot_sb(hies):
#     """
#     Plot all the defined objects
#     """

#     for hie in hies:
#         plot_sb_by_hie(hie)

def plot_sb_ax(ax, hies, palette=None):
    """
    Plot all the defined objects for all the provided hierarchies.

    Parameters:
        ax:
            The axis object
        hies: List of integers.
            Hierarchies to be plotted.
        palette: Dictionary
            A dictionary containing the codes corresponding to each SB.
    """

    for hie in hies:
        plot_sb_by_hie_ax(ax, hie, palette)

def plot_sb_fig(fig, hies, palette=None):
    """
    Plot all the defined objects for all the provided hierarchies.

    Parameters:
        fig:
            The axis object
        hies: List of integers.
            Hierarchies to be plotted.
        palette: Dictionary
            A dictionary containing the codes corresponding to each SB.
    """

    axs = [None]*len(hies)
    for i, hie in enumerate(hies):
        axs[i] = fig.add_subplot(label="{0}".format(hie))
        plot_sb_by_hie_ax(axs[i], hie, palette)
    return(axs)
    
def get_newer_sb_same_hie(sb):
    """
    Get all the defined SBs with the same hierarchy but
    of greater chronology.

    Parameters:
        sb: SBound
            The interested SB.
    """
    # Maybe better include this as a method of SBound class?
    # Is this still used/useful?
    
    # Get all the objects with same hierarchy
    sbobjs = get_sbobj_by_hie(sb.hierarchy)
    sb_ok = [x for x in sbobjs if x.parent == sb.parent] 
    i_obj = [i for i,obj in enumerate(sb_ok) if obj == sb][0]
    return(sb_ok[i_obj+1:])
    
    
def get_bot_sb(sb, sbs):
    """
    Get a list of SB objects that are potential candidates to
    provide the bottom for the given SB.

    Parameters:
        sb: SBound
        sbs: list of SBound objects
    """
    # OBSOLETE?
    bot_sbs = [x for x in sbs if ((x.hierarchy >= sb.hierarchy) and
                                  (x.chronology <= sb.chronology))]
    return(bot_sbs)


def get_top_sb(sb, sbs):
    """
    Get a list of SB objects that are potential candidates to
    provide the bottom for the given SB

    Parameters:
        sb: SBound
        sbs: list of SBound objects

    """
    top_sbs = [x for x in sbs if ((x.hierarchy >= sb.hierarchy) and
                                  (x.chronology > sb.chronology))]
    return(top_sbs)


def get_intersect(name, data):
    """
    Get a dataframe of points of SBs that intersect with the SB "name".
    If there is no intersection, the output dataframe will be empty.

    Parameters:
        name: 
            Name of the current SB we are working with
        data:
            Dataset containing the point correlations

    Returns:
        A daframe containing the intersection points.
    
    """
    # Find all the duplicates (intersections)
    df_dupl = data[data.duplicated(["x","z"], keep=False)]

    # Select the coordinates of the intersection with the current "name" SB
    x = df_dupl[df_dupl["sb_name"] == name]["x"]
    z = df_dupl[df_dupl["sb_name"] == name]["z"]

    return(df_dupl[df_dupl["x"].isin(x) & df_dupl["z"].isin(z) &
                   (df_dupl["sb_name"]!=name)])

    
def migrate(df, xmesh, zmesh):
    """
    Migrate the "sparse" coordinates of some points contained in the "x" and
    "z" of a DataFrame into the points or a regularly spaced grid.

    Parameters:
        df: pandas DataFrame
            The dataframe containing the coordinates "x" and "z" to be migrated.
        xmesh: "x" output from meshgrid
            A matrix containing the *x* coordinates of a structured grid.
        zmesh: "z" output from meshgrid
            A matrix containing the *z* coordinates of a structured grid.

    """
    print("")
    print('    Migrating "true" coordinates into grid coordinates...')
    for i, row in df.iterrows():
        # Compute the distance
        dist = np.sqrt((xmesh - row["x"])**2+(zmesh - row["z"])**2)
        # Compute the coordinates of the min distance
        coord = np.unravel_index(np.argmin(dist), xmesh.shape)
        # Migrate "sparse" points to structured grid in the DataFrame
        df.loc[i, "xg"] = xmesh[coord]
        df.loc[i, "zg"] = zmesh[coord]

    # Perform a simple check about the number of intersection points in the
    # original data and after the migration
    
    # Number of unique intersection points in the "true" coordinates
    unique_true = df[df.duplicated(["x","z"])].shape[0]
    # Number of unique intersection points in the "grid" coordinates
    unique_grid = df[df.duplicated(["xg","zg"])].shape[0]
    if unique_true == unique_grid:
        print('        OK, number of unique intersection in the "true" coordinates')
        print('        same as "grid" coordinates.')
        print('        nb. of intersections: {0}'.format(unique_true))
    else:
        print('        WARNING: number of intersections with the "true"')
        print('        coordinates differs from "grid" coordinates.')
        print('            nb. of "true" intersections: {0}'.format(unique_true))
        print('            nb. of "grid" intersections: {0}'.format(unique_grid))


def print_start():
    """
    Print a header with the module name and the version.
    """
    print("")
    print("    **************************************************")
    print("    * hiegeo:                                        *")
    print("    *     Constraining geological architectures with *")
    print("    *     - stratigraphic hierarchy and              *")
    print("    *     - chronological relations                  *")
    print("    **************************************************")
    print("")

def check_data_ingrid(data, x, z):
    """
    Check if data are contained in the discretization grid.

    Parameters:
        data: (pandas DataFrame)
            The input data set. See the documentation for more details.
        x, y: numpy arrays
            These are the discretization grid coordinates.

    .. note::
        Actually, the warning message in general is not a "nasty" one, since it only
        states that the definining points of some SBs were not available on all the
        vertical coordinates, and therefore the domain was restricted.
    """
    print("")
    print("    Check if data are contained in the discretization grid...")
    if (data["x"].min() < x[0]  or
        data["x"].max() > x[-1] or
        data["z"].min() < z[0]  or
        data["z"].max() > z[-1]) :
        print("")
        print("        WARNING: some input data are outside the discretization grid.")
        print("            (if you are aware of this you can ignore this warning.)")
        print("")
    else:
        print("        OK: all data included in the discretization grid bounds.")

def print_data_info(data):
    """
    Print some info about the data.
    """
    print("")
    print("    Data set info:")
    print("        x in [{0}, {1}]".format(data["x"].min(), data["x"].max()))
    print("        z in [{0}, {1}]".format(data["z"].min(), data["z"].max()))
    print("        availabe hierarchies: {0}".format(get_unique_hierarchy(data)))
    print("        availabe chronologies: {0}".format(get_unique_chronology(data)))
    print("        total nb.of points: {0}".format(len(data)))
    print("        Defined SBs: {0}".format( get_unique_sb_name(data)))


def get_allmin(sbs):
    """
    Given a list of objects, return the min of the *z* coordinate.

    .. note::
        Warnings about all columns containing a NaN in `nanmin` is suppressed
        as it should not be harmful.
    """
    obj_nb = len(sbs)
    nz = len(sbs[0].zd)

    mins = np.zeros((obj_nb, nz))

    for i, sb in enumerate(sbs):
        mins[i,:] = np.asarray(sb.zd)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = np.nanmin(mins, axis=0)
    return(out)


def plot_su_ax(ax, hierarchy, hie_alpha):
    """
    Plot a SU provided a matplotlib axis.

    Parameters:
        ax: matplotlib axis
            The axis where to plot the SU.
        hierarchy: integer
            The min hierarchy to be plotted.
        hie_alpha: float
            Transparency value
    """
    # Get all the defined SBs with hierarchy>=hierarchy
    # (sorted by chronology)
    sbs = get_sbobj_by_hie(hierarchy, mode="ge")

    # Avoid plotting the last, which is the topography
    for sb in sbs[:-1]:
        sb.plot_fill(ax, hierarchy, hie_alpha[sb.hierarchy])


def get_parent_by_name(data, sb_name):
    """
    Given a data set, find the "parent" SB of a SB with a given name.

    Parameters:
       data: data set (see package documentation for details)
           The data set where to look for parents.
       sb_name: string
           The name of the SB of which looking for a "parent"
    
    Return:
       Name of the parent SB
    """
    sb_hierarchy = get_sb_hierarchy(data, sb_name)
    sb_chronology = get_sb_chronology(data, sb_name)
    try:
        sb_parent = data[np.logical_and(data["hierarchy"]  > sb_hierarchy,
                                        data["chronology"] < sb_chronology)].sort_values(by=["chronology"]).iloc[-1]["sb_name"]
    except IndexError:
        # If the hierarchy of the SB is already the max available, then in
        # principle there should not be any "child". Set to None
        sb_parent = None
        
    return sb_parent

def get_SBparent_by_name(data, sb_name):
    """
    Given a data set, find the "parent" SB of a SB with a given name.

    Parameters:
       data: data set (see package documentation for details)
           The data set where to look for parents.
       sb_name: string
           The name of the SB of which looking for a "parent"
    
    Return:
       The parent object SB
    """
    sb_hierarchy = get_sb_hierarchy(data, sb_name)
    sb_chronology = get_sb_chronology(data, sb_name)
    
    try:
        sb_parent = data[np.logical_and(data["hierarchy"]  > sb_hierarchy,
                                        data["chronology"] < sb_chronology)].sort_values(by=["chronology"]).iloc[-1]["sb_name"]
    except IndexError:
        # If the hierarchy of the SB is already the max available, then in
        # principle there should not be any "child". Set to None
        sb_parent = None
        
    return sb_parent

def get_SU_by_bot(bot):
    """
    Find the SU object corresponding to a given bottom SB.

    .. warning: Under development
    """
    # NOTE:
    #     1) See function `get_sbobj_by_hie` for something similar
    #     2) Maybe, if the SUs are organized in a Dictionary, this
    #        function would not be the best solution to do that...

    # Collect all objects defined in the calling script
    all_obj = gc.get_objects()

    su_obj = []
    
    for obj in all_obj:
        if type(obj) is SUnit:
            #if obj.bot.name == bot.name:
            su_obj.append(obj)

    return(su_obj)
