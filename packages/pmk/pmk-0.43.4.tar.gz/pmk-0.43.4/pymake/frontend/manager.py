import sys, os
import inspect
import fnmatch

from pymake import Model, Corpus
from pymake.core.types import resolve_model_name

from pymake.core.logformatter import logger


class FrontendManager(object):
    """ Utility Class who aims at mananing/Getting the datastructure at the higher level.

        Parameters
        ----------
        get: return a frontend object.
        load: return a frontend object where data are
              loaded and filtered (sampled...) according to expe.
    """

    log = logger

    _frontend_ext = ['gt', # graph-tool
                     'pk', # pickle
                    ]
    #_model_ext = @Todo: dense(numpy/pk.gz) or sparse => gt...?

    @classmethod
    def load(cls, expe, skip_init=False):
        """ Return the frontend suited for the given expe
            @TODO: skip_init is not implemented

        """
        if skip_init:
            cls.log.warning('skip init is not implemented')

        corpus_name = expe.get('corpus') or expe.get('random') or expe.get('concept')
        if expe.get('driver'):
            corpus_name += '.' + expe.driver.strip('.')

        if '.' in corpus_name:
            c_split = corpus_name.split('.')
            c_name, c_ext = '.'.join(c_split[:-1]), c_split[-1]
        else:
            c_name = corpus_name
            c_ext = None

        _corpus = Corpus.get(c_name)
        if c_ext in cls._frontend_ext:
            # graph-tool object
            # @Todo: Corpus integration!
            if not _corpus:
                dt_lut = {'gt': 'network'}
                _corpus = dict(data_type=dt_lut[c_ext])
            _corpus.update(data_format=c_ext)
        elif _corpus is False:
            raise ValueError('Unknown Corpus `%s\'!' % c_name)
        elif _corpus is None:
            return None

        if _corpus['data_type'] == 'text':
            from .frontendtext import frontendText
            frontend = frontendText(expe)
        elif _corpus['data_type'] == 'network':
            if _corpus.get('data_format') == 'gt':
                from .frontendnetwork import frontendNetwork_gt
                frontend = frontendNetwork_gt.from_expe(expe, corpus=_corpus)
            else:
                from .frontendnetwork import frontendNetwork
                # Obsolete loading design. @Todo
                frontend = frontendNetwork(expe)
                frontend.load_data(randomize=False)

        if hasattr(frontend, 'configure'):
            frontend.configure()

        return frontend


class ModelManager(object):
    """ Utility Class for Managing I/O and debugging Models

        Notes
        -----
        This class is more a wrapper or a **Meta-Model**.
    """

    log = logger

    def __init__(self, expe=None):
        self.expe = expe

    def is_model(self, m, _type):
        if _type == 'pymake':
            # __init__ method should be of type (expe, frontend, ...)
            pmk = inspect.signature(m).parameters.keys()
            score = []
            for wd in ('frontend', 'expe'):
                score.append(wd in pmk)
            return all(score)
        else:
            raise ValueError('Model type unkonwn: %s' % _type)

    @staticmethod
    def model_walker(bdir, fmt='list'):
        models_files = []
        if fmt == 'list':
            ### Easy formating
            for root, dirnames, filenames in os.walk(bdir):
                for filename in fnmatch.filter(filenames, '*.pk*'):
                    models_files.append(os.path.join(root, filename))
            return models_files
        else:
            ### More Complex formating
            tree = {'json': [],
                    'pk': [],
                    'inference': []}
            for filename in fnmatch.filter(filenames, '*.pk'):
                if filename.startswith(('dico.', 'vocab.')):
                    dico_files.append(os.path.join(root, filename))
                else:
                    corpus_files.append(os.path.join(root, filename))
            raise NotImplementedError()
        return tree

    def _get_model(self, frontend=None, model=None):
        ''' Get model with lookup in the following order :
            * pymake.model
            * mla (todo)
            * scikit-learn (see Sklearn wraper)

            Params
            ------
            :frontend: Input data
            :model: The name of the model. (self.expe.model if None)
        '''

        model_name = self.expe.model if model is None else resolve_model_name(model)

        # @@@@Debug model and model ref name (resolve_model_name
        # + implement dict value for model (or in list of model, in order to
        #   1. ba able to describe params in a better way
        #   2. propagate _default_spec from pymake
        if isinstance(model_name, str):
            _model = Model.get(model_name)
        elif isinstance(model_name, list):
            # Sklearn Pipeline
            # # @debug cant be pickled like this !
            from pymake.model import ModelSkl
            modules = []
            for m in model_name:
                submodel = Model.get(m)
                if not submodel:
                    self.log.error('Model Unknown : %s' % (m))
                    raise NotImplementedError(m)
                modules.append(submodel.module)

            model_name = '-'.join(model_name)
            _model = type(model_name, (ModelSkl,), {'module': modules})

        else:
            raise ValueError('Type of model unknow: %s | %s' % (type(model_name), model_name))

        if not _model:
            self.log.error('Model Unknown : %s' % (model_name))
            raise NotImplementedError(model_name)

        # @Improve: * initialize all model with expe
        #           * fit with frontend, transform with frontend (as sklearn do)
        if self.is_model(_model, 'pymake'):
            model = _model(self.expe, frontend)
        else:
            model = _model(self.expe)

        return model

    @classmethod
    def _load_model(cls, fn):
        import pymake.io as io

        _fn = io.resolve_filename(fn)
        if not os.path.isfile(_fn):
            # io integration?
            _fn += '.gz'

        if not os.path.isfile(_fn) or os.stat(_fn).st_size == 0:
            cls.log.error('No file for this model : %s' % _fn)

            cls.log.trace('The following are available :')
            for f in cls.model_walker(os.path.dirname(_fn), fmt='list'):
                cls.log.trace(f)
            return

        cls.log.info('Loading Model: %s' % fn)
        model = io.load(fn, silent=True)

        return model

    @staticmethod
    def update_expe(expe, model):
        ''' Configure some pymake settings if present in model. '''

        pmk_settings = ['_measures', '_fmt']

        for _set in pmk_settings:
            if getattr(model, _set, None) and not expe.get(_set):
                expe[_set] = getattr(model, _set)

    @classmethod
    def from_expe(cls, expe, frontend=None, model=None, load=False):
        # frontend params is deprecated and will be removed soon...

        if load is False:
            mm = cls(expe)
            model = mm._get_model(frontend=frontend, model=model)
        else:
            fn = expe._output_path
            model = cls._load_model(fn)

        cls.update_expe(expe, model)

        return model
