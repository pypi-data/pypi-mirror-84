import os
from applycal import applycal
from plotcal import plotcal
from polcal import polcal
from applycal import applycal
from gaincal import gaincal

class PolCalibration(object):
    def __init__(self, vis="", spw_ids=np.array([]), polanglefield="", leakagefield="", target="", refant="", calibration_tables=[], **kwargs):
        initlocals = locals()
        initlocals.pop('self')
        for a_attribute in initlocals.keys():
            setattr(self, a_attribute, initlocals[a_attribute])
        self.__dict__.update(kwargs)
        self.nspw = len(spw_ids)


    def setModel(self, pol_source_object = None, standard="Perley-Butler 2013", field="", epoch="2012", nu_0=0.0, nterms_angle=3, nterms_frac=3, nu_min=0.0, nu_max=np.inf):

        # get spectral idx coeffs from VLA tables
        pol_source_object.getCoeffs(standard=standard, epoch=epoch)
        nu_fit = np.linspace(0.3275*1e9, 50.0*1e9, 40)
        spec_idx = pol_source_object.fitAlphaBeta(nu_fit, nu_0=nu_0)
        pol_frac_coeffs = pol_source_object.getPolFracCoeffs(nu_0=nu_0, nterms=nterms_frac, nu_min=nu_min, nu_max=nu_max)
        pol_angle_coeffs = pol_source_object.getPolAngleCoeffs(nu_0=nu_0, nterms=nterms_angle, nu_min=nu_min, nu_max=nu_max)
        # get intensity in reference frequency
        intensity = pol_source_object.flux_scalar(nu_0/1e9)
        setjy(vis=self.vis, field=field, standard='manual', spw="*", fluxdensity=[intensity,0,0,0], spix=spec_idx, reffreq=str(nu_0/1e9)+"GHz", polindex=pol_frac_coeffs, polangle=pol_angle_coeffs, scalebychan=True, usescratch=False)

    def calibrateLeakage(self, minsnr=3, poltype="Df", caltable="D0", gaintable=[]):
        if os.path.exists(caltable): rmtables(caltable)
        polcal(vis=self.vis, caltable=caltable, field=self.leakagefield, spw='', refant=self.refant, poltype=poltype, solint='inf', combine='scan', minsnr=minsnr, gaintable=gaintable)
        return caltable

    def calibratePolAngle(self, minsnr=3, caltable="X0", poltype="Xf", gaintable=[]):
        if os.path.exists(caltable): rmtables(caltable)
        polcal(vis=self.vis, caltable=caltable, field=self.polanglefield, spw='', refant=self.refant, poltype=poltype, solint='inf', combine='scan', minsnr=minsnr, gaintable=gaintable)
        return caltable

    def plotLeakage(self, leakagecaltable="DO", plotdir=""):
        plotcal(caltable=leakagecaltable, xaxis='antenna', yaxis='amp', figfile=plotdir+self.vis[:-3]+'.D0.amp.png', showgui=False)
        plotcal(caltable=leakagecaltable, xaxis='antenna', yaxis='phase', iteration='antenna', figfile=plotdir+self.vis[:-3]+'.D0.phs.png', showgui=False)
        plotcal(caltable=leakagecaltable, xaxis='antenna', yaxis='snr', showgui=False, figfile=plotdir+self.vis[:-3]+'.D0.snr.png')
        plotcal(caltable=leakagecaltable, xaxis='real', yaxis='imag', showgui=False, figfile=plotdir+self.vis[:-3]+'.D0.cmplx.png')

    def applySolutions(self, gaintables=[]):
        spw = np.array2string(self.spw_ids, separator=',').replace("[", "").replace("]","")
        applycal(vis=self.vis, field=self.polanglefield, spw=spw, gaintable=alltables, calwt=[False], parang=True)
        applycal(vis=self.vis, field=self.leakagefield, spw=spw, gaintable=alltables, calwt=[False], parang=True)
        applycal(vis=self.vis, field=self.target, spw=spw, gaintable=alltables, calwt=[False], parang=True)

    #def calibrate(self, known_pol_object=None, standard="Perley-Butler 2013", epoch="2012", plotdir="", nu_0=0.0, nterms_angle=3, nterms_frac=3):
    #    self.setModel(pol_source_object=known_pol_object, standard=standard, field=self.bcal, epoch=epoch, nu_0=nu_0, nterms_angle=nterms_angle, nterms_frac=nterms_frac)
    #    self.setModel(pol_source_object=known_pol_object, standard=standard, field=self.lcal, epoch=epoch, nu_0=nu_0, nterms_angle=nterms_angle, nterms_frac=nterms_frac)
    #    leakage_table = self.calibrateLeakage()
    #    self.plotLeakage(plotdir=plotdir)
    #    polangle_table = self.calibratePolAngle()
    #    self.applySolutions()
