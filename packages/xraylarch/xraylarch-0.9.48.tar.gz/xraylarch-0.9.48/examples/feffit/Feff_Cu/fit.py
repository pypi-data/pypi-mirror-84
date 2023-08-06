## Larch Script for Fitting Cu XAFS
# read data, perform background subtraction
from larch import Group as group
from larch.fitting import guess
from larch.io import read_xdi
from larch.xafs import (autobk, feffit, feffpath,
                        feffit_transform, feffit_dataset)
from larch.wxlib.xafsplots import plot_chifit


cu_data = read_xdi('cu_metal_rt.xdi')
cu_data.mu = cu_data.mutrans
autobk(cu_data, rbkg=1.2, kw=2)

# define fitting parameter group
fit_params=group(s02   = guess(1),
                 e0    = guess(4),
                 alpha = guess(0),
                 c3_p1 = guess(0),
                 ss2_p1= guess(0.002),
                 ss2_p2= guess(0.002),
                 ss2_p3= guess(0.002),
                 ss2_p4= guess(0.002),
                 ss2_p6= guess(0.002) )


# define a list of Feff Paths and Path Parameters
paths = [feffpath('feff0001.dat', sigma2='ss2_p1',
                 third='c3_p1', s02='s02', e0='e0',
                 deltar='alpha*reff')]
for fpath, s2var in (('02', 'p2'), ('03', 'p3'),
           ('04', 'p4'), ('05', 'p4'), ('06', 'p6'),
           ('07', 'p6'), ('08', 'p4'), ('09', 'p4'),
           ('10', 'p4'), ('11', 'p4'), ('12', 'p4'),
           ('13', 'p4')):
     paths.append(feffpath('feff00%s.dat' % fpath,
                           sigma2='ss2_%s' % s2var,
                           s02='s02', e0='e0',
                           deltar='alpha*reff'))

#endfor

# set FT parameters, window function, fit ranges
trans= feffit_transform(kmin=3, kmax=16, kw=2, dk=5,
          window='kaiser', rmin=1.3, rmax=4.8)

# define dataset with data, transform, path list

dset = feffit_dataset(data=cu_data, transform=trans, pathlist=paths)

# perform fit, show results
result = feffit(fit_params, dset)

print(feffit_report(result))

plot_chifit(dset, show_imag=True, rmax=6.5)

# plot_axvline(1.3, win=2)
# plot_axvline(4.8, win=2)
# i1 = index_of(dset.data.r, 1.3)
# i2 = index_of(dset.data.r, 4.8)
# plot(dset.data.r[i1:i2],
#      -3+(dset.data.chir_im-dset.model.chir_im)[i1:i2],
#xq     sytle='short dashed', win=2)



def tweak_display():
    disp = get_display()
    disp.Size = (550, 450)
    disp.Size = (548, 450)
    panel  = disp.panel
    canvas = panel.canvas
    canvas.figure.set_facecolor('white')
    ax = panel.axes
    ax.set_facecolor('white')
    canvas.draw()

    ax.figbox.p0 = array([0.175, 0.175])
    ax.figbox.p1 = array([0.90, 0.95])
    ax.set_position(ax.figbox)
    return disp
#enddef

irmin  = index_of(dset.data.r, 1.3)
irmax  = index_of(dset.data.r, 4.8)

fopts = dict(linewidth=3, style='short dashed', color='black', zorder=50, fullbox=False)
dopts = dict(linewidth=3, style='solid',        color='blue', zorder=1, fullbox=False, grid=False)

cshade='#FAFAFA'
cedge='#D0D0D0'
dopts['color'] = 'black'

plot(dset.data.r,  dset.data.chir_im, new=True, xmax=6.3,
     ymin=-3.75, ymax=3.25,
     xlabel=r'$R \rm\,(\AA)$', ylabel=r'$\chi(R)\rm\,(\AA^{-3})$',
     show_grid=False, **dopts)
plot(dset.model.r, dset.model.chir_im, **fopts)
plot(dset.data.r, dset.data.chir_mag,  **dopts)

panel= get_display().panel
panel.axes.axvspan(1.3, 4.8, facecolor=cshade, edgecolor=cedge)
plot_text( r'${\rm \Delta \, Im}[\chi(R)]$ ', 3.05, -2.45)
plot(dset.model.r[irmin:irmax], -3.0 + (dset.model.chir_re-dset.data.chir_re)[irmin:irmax], **fopts)

tweak_display()
save_plot('fit_r.png')


fopts = dict(linewidth=3, style='short dashed', color='black', zorder=50, fullbox=False)
dopts = dict(linewidth=3, style='solid',  color='blue', zorder=1, fullbox=False, grid=False)
dopts['color'] = 'black'
k = dset.data.k
plot(k,  dset.data.chi*k**2, new=True, xmax=17,
     xlabel=r'$k\rm\,(\AA^{-1})$',
     ylabel=r'$k^2\chi(k)\rm\,(\AA^{-2})$',
     show_grid=False,
     **dopts)
plot(k, dset.model.chi*k**2, **fopts)
tweak_display()
save_plot('fit_k.png')
