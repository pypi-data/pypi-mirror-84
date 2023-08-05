import os, re

import pandas as pd

from .utils import decode_harmonies, no_collections_no_booleans, resolve_dir, update_labels_cfg, update_cfg
from .bs4_parser import _MSCX_bs4
from .annotations import Annotations
from .logger import LoggedClass




class Score(LoggedClass):
    """ Object representing a score.

    Attributes
    ----------
    infer_label_types : :obj:`list` or :obj:`dict`, optional
        Changing this value results in a call to :py:meth:`~ms3.annotations.Annotations.infer_types`.
    logger : :obj:`logging.Logger` or :obj:`logging.LoggerAdapter`
        Current logger that the object is using.
    parser : {'bs4'}
        The only XML parser currently implemented is BeautifulSoup 4.
    paths, files, fnames, fexts, logger_names : :obj:`dict`
        Dictionaries for keeping track of file information handled by :py:meth:`~ms3.score.Score.handle_path`.




    Methods
    -------
    handle_path(path, key)
        Puts the path into `paths, files, fnames, fexts` dicts with the given key.

    """

    abs_regex = r"^\(?[A-G|a-g](b*|#*).*?(/[A-G|a-g](b*|#*))?$"

    dcml_regex = re.compile(r"""
                                ^(?P<first>
                                  (\.?
                                    ((?P<globalkey>[a-gA-G](b*|\#*))\.)?
                                    ((?P<localkey>(b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i))\.)?
                                    ((?P<pedal>(b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i))\[)?
                                    (?P<chord>
                                        (?P<numeral>(b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i|Ger|It|Fr|@none))
                                        (?P<form>(%|o|\+|M|\+M))?
                                        (?P<figbass>(7|65|43|42|2|64|6))?
                                        (\((?P<changes>((\+|-|\^)?(b*|\#*)\d)+)\))?
                                        (/(?P<relativeroot>((b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i)/?)*))?
                                    )
                                    (?P<pedalend>\])?
                                  )?
                                  (?P<phraseend>(\\\\|\{|\}|\}\{)
                                  )?
                                 )
                                 (-
                                  (?P<second>
                                    ((?P<globalkey2>[a-gA-G](b*|\#*))\.)?
                                    ((?P<localkey2>(b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i))\.)?
                                    ((?P<pedal2>(b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i))\[)?
                                    (?P<chord2>
                                        (?P<numeral2>(b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i|Ger|It|Fr|@none))
                                        (?P<form2>(%|o|\+|M|\+M))?
                                        (?P<figbass2>(7|65|43|42|2|64|6))?
                                        (\((?P<changes2>((\+|-|\^)?(b*|\#*)\d)+)\))?
                                        (/(?P<relativeroot2>((b*|\#*)(VII|VI|V|IV|III|II|I|vii|vi|v|iv|iii|ii|i)/?)*))?
                                    )
                                    (?P<pedalend2>\])?
                                  )?
                                  (?P<phraseend2>(\\\\|\{|\}|\}\{)
                                  )?
                                 )?
                                $
                                """,
                            re.VERBOSE)

    nashville_regex = r"^(b*|#*)(\d).*$"

    rn_regex = r"^$"

    def __init__(self, mscx_src=None, infer_label_types=['dcml'], read_only=False, labels_cfg={}, logger_cfg={}, parser='bs4'):
        """

        Parameters
        ----------
        mscx_src : :obj:`str`, optional
            Path to the MuseScore file to be parsed.
        infer_label_types : :obj:`list` or :obj:`dict`, optional
            Determine which label types are determined automatically. Defaults to ['dcml'].
            Pass ``[]`` to infer only main types 0 - 3.
            Pass ``{'type_name': r"^(regular)(Expression)$"}`` to call :meth:`ms3.Score.new_type`.
        read_only : :obj:`bool`, optional
            Defaults to ``False``, meaning that the parsing is slower and uses more memory in order to allow for manipulations
            of the score, such as adding and deleting labels. Set to ``True`` if you're only extracting information.
        logger_cfg : :obj:`dict`, optional
            The following options are available:
            'name': LOGGER_NAME -> by default the logger name is based on the parsed file(s)
            'level': {'W', 'D', 'I', 'E', 'C', 'WARNING', 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'}
            'file': PATH_TO_LOGFILE to store all log messages under the given path.
        parser : {'bs4'}, optional
            The only XML parser currently implemented is BeautifulSoup 4.
        """
        super().__init__(subclass='Score', logger_cfg=logger_cfg)
        self.full_paths, self.paths, self.files, self.fnames, self.fexts = {}, {}, {}, {}, {}
        self._mscx = None
        self._annotations = {}
        self._types_to_infer = []
        self._label_types = {
            0: "Simple string (should not begin with a note name, otherwise MS3 will turn it into type 3; prevent through leading dot)",
            1: "MuseScore's Roman Numeral Annotation format",
            2: "MuseScore's Nashville Number format",
            3: "Absolute chord encoded by MuseScore",
            'dcml': "Latest version of the DCML harmonic annotation standard.",
        }
        self._harmony_regex = {
            1: self.rn_regex,
            2: self.nashville_regex,
            3: self.abs_regex,
            'dcml': self.dcml_regex,
        }
        self.infer_label_types = infer_label_types
        self.parser = parser
        if mscx_src is not None:
            self._parse_mscx(mscx_src, read_only=read_only, labels_cfg=labels_cfg)

    @property
    def infer_label_types(self):
        return self._types_to_infer

    @infer_label_types.setter
    def infer_label_types(self, val):
        if val is None:
            val = []
        before_inf, before_reg = self._types_to_infer, self.get_infer_regex()
        if isinstance(val, list):
            exist = [v for v in val if v in self._harmony_regex]
            if len(exist) < len(val):
                logger.warning(f"The following harmony types have not been added via the new_type() method:\n{[v for v in val if v not in self._harmony_regex]}")
            self._types_to_infer = exist
        elif isinstance(val, dict):
            for k, v in val.items():
                if k in self._harmony_regex:
                    if v is None:
                        val[k] = self._harmony_regex[k]
                    else:
                        self._harmony_regex[k] = v
                else:
                    self.new_type(name=k, regex=v)
            self._types_to_infer = list(val.keys())
        after_reg = self.get_infer_regex()
        if before_inf != self._types_to_infer or before_reg != after_reg:
            for ann in self._annotations.values():
                ann.infer_types(after_reg)


    def get_infer_regex(self):
        return {t: self._harmony_regex[t] for t in self._types_to_infer}



    def handle_path(self, path, key=None):
        full_path = resolve_dir(path)
        if os.path.isfile(full_path):
            file_path, file = os.path.split(full_path)
            file_name, file_ext = os.path.splitext(file)
            if key is None:
                key = file_ext[1:]
            elif key == 'file':
                key = file
            self.full_paths[key] = full_path
            self.paths[key] = file_path
            self.files[key] = file
            self.fnames[key] = file_name
            self.fexts[key] = file_ext
            self.logger_names[key] = file_name.replace('.', '')
            return key
        else:
            self.logger.error("No file found at this path: " + full_path)
            return None



    def _parse_mscx(self, mscx_src, read_only=False, parser=None, labels_cfg={}):
        """
        This method is called by :meth:`.__init__` to parse the score.
        It doesn't systematically clean up data from previous parse.

        """
        _ = self.handle_path(mscx_src)
        if parser is not None:
            self.parser = parser
        if 'mscx' in self.fnames:
            logger_cfg = self.logger_cfg.copy()
            logger_cfg['name'] = self.logger_names['mscx']
            self._mscx = MSCX(self.full_paths['mscx'], read_only=read_only, labels_cfg=labels_cfg, parser=self.parser, logger_cfg=logger_cfg)
            if self._mscx.has_annotations:
                self._annotations['annotations'] = self._mscx._annotations
                self._annotations['annotations'].infer_types(self.get_infer_regex())
        else:
            self.logger.error("No existing .mscx file specified.")

    def store_mscx(self, filepath):
        return self._mscx.store_mscx(filepath)

    def detach_labels(self, key, staff=None, voice=None, label_type=None, delete=True):
        if 'annotations' not in self._annotations:
            self.logger.info("No annotations present in score.")
            return
        assert key != 'annotations', "The key 'annotations' is reserved, please choose a different one."
        if not key.isidentifier():
            self.logger.warning(f"'{key}' can not be used as an identifier. The extracted labels need to be accessed via self._annotations['{key}']")
        df = self.annotations.get_labels(staff=staff, voice=voice, label_type=label_type, drop=delete)
        if len(df) == 0:
            self.logger.info(f"No labels found for staff {staff}, voice {voice}, label_type {label_type}.")
            return
        logger_cfg = self.logger_cfg.copy()
        logger_cfg['name'] += f"{self.logger_names['mscx']}:{key}"
        self._annotations[key] = Annotations(df=df, infer_types=self.get_infer_regex(), mscx_obj=self._mscx, logger_cfg=logger_cfg)
        if delete:
            self._mscx.delete_labels(df)
        if len(self._annotations['annotations'].df) == 0:
            self._mscx.has_annotations = False
            del (self._annotations['annotations'])
        return


    def attach_labels(self, key, staff=None, voice=None, check_for_clashes=True):
        """ Insert detached labels ``key`` into this score.

        Parameters
        ----------
        key : :obj:`str`
            Key of the detached labels you want to insert into the score.
        staff, voice : :obj:`int`, optional
            Pass one or both of these arguments to change the original annotation layer or if there was none.
        check_for_clashes : :obj:`bool`, optional
            Defaults to True, meaning that the positions where the labels will be inserted will be checked for existing
            labels.

        Returns
        -------
        :obj:`int`
            Number of newly attached labels.
        :obj:`int`
            Number of labels that were to be attached.
        """
        assert key != 'annotations', "Labels with key 'annotations' are already attached."
        if key not in self._annotations:
            self.logger.info(f"""Key '{key}' doesn't correspond to a detached set of annotations.
Use on of the existing keys or load a new set with the method load_annotations().\nExisting keys: {list(self._annotations.keys())}""")
            return 0, 0

        annotations = self._annotations[key]
        goal = len(annotations.df)
        if goal == 0:
            self.logger.warning(f"The Annotation object '{key}' does not contain any labels.")
            return 0, 0
        df = annotations.prepare_for_attaching(staff=staff, voice=voice, check_for_clashes=check_for_clashes)
        reached = len(df)
        if reached == 0:
            self.logger.error(f"No labels from '{key}' have been attached due to aforementioned errors.")
            return reached, goal

        reached = self._mscx.add_labels(df, label=annotations.cols['label'])
        self._annotations['annotations'] = self._mscx._annotations
        if len(self._mscx._annotations.df) > 0:
            self._mscx.has_annotations = True
        return reached, goal


    @property
    def has_detached_annotations(self):
        return sum(True for key in self._annotations if key != 'annotations') > 0


    @property
    def mscx(self):
        """ Returns the `MSCX` object with the parsed score.
        """
        if self._mscx is None:
            raise LookupError("No XML has been parsed so far. Use the method parse_mscx().")
        return self._mscx


    def load_annotations(self, tsv_path=None, anno_obj=None, key='file', cols={}, infer=True):
        """ Create an Annotations object from a tsv file and make it available as Score.key """
        assert sum(True for arg in [tsv_path, anno_obj] if arg is not None) == 1, "Pass either tsv_path or anno_obj."
        inf_dict = self.get_infer_regex() if infer else {}
        mscx = None if self._mscx is None else self._mscx
        if tsv_path is not None:
            key = self.handle_path(tsv_path, key)
            logger_cfg = self.logger_cfg.copy()
            logger_cfg['name'] = f"{self.logger_names[key]}"
            self._annotations[key] = Annotations(tsv_path=tsv_path, infer_types=inf_dict, cols=cols, mscx_obj=mscx, logger_cfg=logger_cfg)
        else:
            anno_obj.mscx_obj = mscx
            self._annotations[key] = anno_obj


    def store_annotations(self, key=None, tsv_path=None, **kwargs):
        """ Save a set of annotations as TSV file. While ``store_list`` stores attached labels only, this method
        can also store detached labels by passing a ``key``. """
        if key is None:
            assert self._mscx.has_annotations, "Score has no labels attached."
            key = 'annotations'
        if tsv_path is None:
            path = self.paths['mscx']
            fname = self.fnames['mscx']
            tsv_path = os.path.join(path, fname + '_labels.tsv')
        assert key in self._annotations, f"Key '{key}' not found. Available keys: {list(self._annotations.keys())}"
        if self._annotations[key].store_tsv(tsv_path, **kwargs):
            new_key = self.handle_path(tsv_path, key=key)
            if key != 'annotations':
                self._annotations[key].update_logger_cfg({'name': self.logger_names[new_key]})


    def __repr__(self):
        msg = ''
        if 'mscx' in self.full_paths:
            msg = f"MuseScore file"
            if self._mscx.changed:
                msg += " (CHANGED!!!)\n---------------!!!!!!!!!!!!"
            else:
                msg += "\n--------------"
            msg += f"\n\n{self.full_paths['mscx']}\n\n"
        if 'annotations' in self._annotations:
            msg += f"Attached annotations\n--------------------\n\n{self.annotations}\n\n"
        else:
            msg += "No annotations attached.\n\n"
        if self.has_detached_annotations:
            msg += "Detached annotations\n--------------------\n\n"
            for key, obj in self._annotations.items():
                if key != 'annotations':
                    key_info = key + f" (stored as {self.files[key]})" if key in self.files else key
                    msg += f"{key_info} -> {obj}\n\n"
        return msg



    @property
    def types(self):
        return self._label_types

    def new_type(self, name, regex, description='', infer=True):
        assert name not in self._label_types, f"'{name}' already added to types: {self._label_types[name]}"
        self._label_types[name] = description
        self._harmony_regex[name] = regex
        if infer:
            self._types_to_infer.insert(0, name)
            for ann in self._annotations.values():
                ann.infer_types(self.get_infer_regex())

    def __getattr__(self, item):
        try:
            return self._annotations[item]
        except:
            raise AttributeError(item)

    def __getitem__(self, item):
        try:
            return self._annotations[item]
        except:
            raise AttributeError(item)




    # def __setattr__(self, key, value):
    #     assert key != 'annotations', "The key 'annotations' is managed automatically, please pick a different one."
    #     assert key.isidentifier(), "Please use an alphanumeric key without special characters."
    #     if key in self.__dict__:
    #         self.__dict__[key] = value
    #     else:
    #         self._annotations[key] = value

class MSCX(LoggedClass):
    """ Object for interacting with the XML structure of a MuseScore 3 file.

    Attributes
    ----------
    mscx_src : :obj:`str`
        MuseScore 3 file to parse.
    _parsed : :obj:`_MSCX_bs4`
        Holds the MSCX score parsed by the selected parser.
    parser : :obj:`str`, optional
        Which XML parser to use.
    infer_label_types :obj:`bool`, optional
        For label_type 0 (simple string), mark which ones
    logger_cfg : :obj:`dict`, optional
        The following options are available:
        'name': LOGGER_NAME -> by default the logger name is based on the parsed file(s)
        'level': {'W', 'D', 'I', 'E', 'C', 'WARNING', 'DEBUG', 'INFO', 'ERROR', 'CRITICAL'}
        'file': PATH_TO_LOGFILE to store all log messages under the given path.

    Methods
    -------
    output_mscx(filepath)
        Write the internal score representation to a file.
    """

    def __init__(self, mscx_src=None, read_only=False, parser='bs4', labels_cfg={}, logger_cfg={}, level=None):
        super().__init__(subclass='MSCX', logger_cfg=logger_cfg)
        self.mscx_src = mscx_src
        self.read_only = read_only
        self._annotations = None
        if parser is not None:
            self.parser = parser
        self._parsed = None
        self.changed = False
        self.store_mscx = None
        self.get_chords = None
        self.get_raw_labels = None
        self.metadata = None
        self.has_annotations = None
        self.infer_mc = None
        self.labels_cfg = {
            'staff': None,
            'voice': None,
            'label_type': None,
            'positioning': True,
            'decode': False,
            'column_name': 'label',
            }
        self.labels_cfg.update(update_labels_cfg(labels_cfg, logger=self.logger))

        if self.mscx_src is not None:
            self.parse_mscx()


    def change_labels_cfg(self, labels_cfg={}, staff=None, voice=None, label_type=None, positioning=None, decode=None):
        for k in self.labels_cfg.keys():
            val = locals()[k]
            if val is not None:
                labels_cfg[k] = val
        self.labels_cfg.update(update_labels_cfg(labels_cfg), logger=self.logger)



    def parse_mscx(self, mscx_src=None):
        if mscx_src is not None:
            self.mscx_src = mscx_src
        assert self.mscx_src is not None, "No path specified for parsing MSCX."
        assert os.path.isfile(self.mscx_src), f"{self.mscx_src} does not exist."

        implemented_parsers = ['bs4']
        if self.parser == 'bs4':

            self._parsed = _MSCX_bs4(self.mscx_src, read_only=self.read_only, logger_cfg=self.logger_cfg)
        else:
            raise NotImplementedError(f"Only the following parsers are available: {', '.join(implemented_parsers)}")

        self.store_mscx = self._parsed.store_mscx
        self.get_chords = self._parsed.get_chords
        self.get_raw_labels = self._parsed.get_raw_labels
        self.metadata = self._parsed.metadata
        self.has_annotations = self._parsed.has_annotations
        self.infer_mc = self._parsed.infer_mc

        if self._parsed.has_annotations:
            logger_cfg = self.logger_cfg.copy()
            logger_cfg['name'] += ':annotations'
            self._annotations = Annotations(df=self.get_raw_labels(), read_only=True, mscx_obj=self, logger_cfg=logger_cfg)


    def delete_labels(self, df):
        changed = pd.Series([self._parsed.delete_label(mc, staff, voice, mc_onset)
                               for mc, staff, voice, mc_onset
                               in reversed(list(df[['mc', 'staff', 'voice', 'mc_onset']].itertuples(name=None, index=False)))],
                            index=df.index)
        changes = changed.sum()
        if changes > 0:
            self.changed = True
            self._parsed.parse_measures()
            target = len(df)
            self.logger.debug(f"{changes}/{target} labels successfully deleted.")
            if changes < target:
                self.logger.warning(f"{target - changes} labels have not been deleted:\n{df.loc[~changed]}")



    def add_labels(self, df, label='label', mc='mc', mc_onset='mc_onset', staff='staff', voice='voice', **kwargs):
        """


        Parameters
        ----------
        df : :obj:`pandas.DataFrame`
            DataFrame with labels to be added.
        label, mc, mc_onset, staff, voice : :obj:`str`
            Names of the DataFrame columns for the five required parameters.
        kwargs:
            label_type, root, base, leftParen, rightParen, offset_x, offset_y, nashville
                For these parameters, the standard column names are used automatically if the columns are present.
                If the column names have changed, pass them as kwargs, e.g. ``base='name_of_the_base_column'``

        Returns
        -------
        :obj:`int`
            Number of actually added labels.

        """
        if len(df) == 0:
            self.logger.info("Nothing to add.")
            return
        cols = dict(
            label_type='label_type',
            root='root',
            base='base',
            leftParen='leftParen',
            rightParen='rightParen',
            offset_x='offset:x',
            offset_y='offset:y',
            nashville='nashville',
            decoded='decoded'
        )
        missing_add = {k: v for k, v in kwargs.items() if v not in df.columns}
        if len(missing_add) > 0:
            self.logger.warning(f"The following specified columns could not be found:\n{missing_add}.")
        main_params = ['label', 'mc', 'mc_onset', 'staff', 'voice']
        l = locals()
        missing_main = {k: l[k] for k in main_params if l[k] not in df.columns}
        assert len(missing_main) == 0, f"The specified columns for the following main parameters are missing:\n{missing_main}"
        main_cols = {k: l[k] for k in main_params}
        cols.update(kwargs)
        if cols['decoded'] not in df.columns:
            df[cols['decoded']] = decode_harmonies(df, label_col=label, return_series=True)
        add_cols = {k: v for k, v in cols.items() if v in df.columns}
        param2cols = {**main_cols, **add_cols}
        parameters = list(param2cols.keys())
        columns = list(param2cols.values())
        self.logger.debug(f"add_label() will be called with this param2col mapping:\n{param2cols}")
        tups = tuple(df[columns].itertuples(index=False, name=None))
        params = [{a: b for a, b in zip(parameters, t)} for t in tups]
        res = [self._parsed.add_label(**p) for p in params]
        changes = sum(res)
        # changes = sum(self.parsed.add_label(**{a: b for a, b in zip(parameters, t)})
        #               for t
        #               in df[columns].itertuples(index=False, name=None)
        #               )
        if changes > 0:
            self.changed = True
            self._parsed.parse_measures()
            logger_cfg = self.logger_cfg.copy()
            logger_cfg['name'] += ':annotations'
            self._annotations = Annotations(df=self.get_raw_labels(), read_only=True, mscx_obj=self, logger_cfg=logger_cfg)
            self.logger.debug(f"{changes}/{len(df)} labels successfully added to score.")
        return changes


    def store_list(self, what='all', folder=None, suffix=None, **kwargs):
        """
        Store one or several several lists as TSV files(s).
        
        Parameters
        ----------
        what : :obj:`str` or :obj:`Collection`, optional
            Defaults to 'all' but could instead be one or several strings out of {'notes', 'rests', 'notes_and_rests', 'measures', 'events', 'labels', 'chords', 'expanded'}
        folder : :obj:`str`, optional
            Where to store. Defaults to the directory of the parsed MSCX file.
        suffix : :obj:`str` or :obj:`Collection`, optional
            Suffix appended to the file name of the parsed MSCX file to create a new file name.
            Defaults to None, meaning that standard suffixes based on ``what`` are attached.
            Number of suffixes needs to be equal to the number of ``what``.
        **kwargs:
            Keyword arguments for :py:meth:`pandas.DataFrame.to_csv`. Defaults to ``{'sep': '\t', 'index': False}``.
            If 'sep' is changed to a different separator, the file extension(s) will be changed to '.csv' rather than '.tsv'.

        Returns
        -------
        None

        """
        folder = resolve_dir(folder)
        mscx_path, file = os.path.split(self.mscx_src)
        fname, _ = os.path.splitext(file)
        if folder is None:
            folder = mscx_path
        if not os.path.isdir(folder):
            if input(folder + ' does not exist. Create? (y|n)') == "y":
                os.mkdir(d)
            else:
                return
        what, suffix = self._treat_storing_params(what, suffix)
        self.logger.debug(f"Parameters normalized to what={what}, suffix={suffix}.")
        if what is None:
            self.logger.error("Tell me 'what' to store.")
            return
        if 'sep' not in kwargs:
            kwargs['sep'] = '\t'
        if 'index' not in kwargs:
            kwargs['index'] = False
        ext = '.tsv' if kwargs['sep'] == '\t' else '.csv'

        for w, s in zip(what, suffix):
            df = self.__getattribute__(w)
            if len(df.index) > 0:
                new_name = f"{fname}{s}{ext}"
                full_path = os.path.join(folder, new_name)
                no_collections_no_booleans(df, logger=self.logger).to_csv(full_path, **kwargs)
                self.logger.info(f"{w} written to {full_path}")
            else:
                self.logger.debug(f"{w} empty, no file written.")





    def _treat_storing_params(self, what, suffix):
        tables = ['notes', 'rests', 'notes_and_rests', 'measures', 'events', 'labels', 'chords', 'expanded']
        if what == 'all':
            if suffix is None:
                return tables, [f"_{t}" for t in tables]
            elif len(suffix) < len(tables) or isinstance(suffix, str):
                self.logger.error(f"If what='all', suffix needs to be None or include one suffix each for {tables}.\nInstead, {suffix} was passed.")
                return None, None
            elif len(suffix) > len(tables):
                suffix = suffix[:len(tables)]
            return tables, [str(s) for s in suffix]

        if isinstance(what, str):
            what = [what]
        if isinstance(suffix, str):
            suffix = [suffix]

        correct = [(i, w) for i, w in enumerate(what) if w in tables]
        if suffix is None:
            suffix = [f"_{w}" for _, w in correct]
        if len(correct) < len(what):
            if len(correct) == 0:
                self.logger.error(f"The value for what can only be out of {['all'] + tables}, not {what}.")
                return None, None
            else:
                incorrect = [w for w in what if w not in tables]
                self.logger.warning(f"The following values are not accepted as parameters for 'what': {incorrect}")
                suffix = [suffix[i] for i, _ in correct]
        if len(correct) < len(suffix):
            self.logger.error(f"Only {len(suffix)} suffixes were passed for storing {len(correct)} tables.")
            return None, None
        elif len(suffix) > len(correct):
            suffix = suffix[:len(correct)]
        return what, [str(s) for s in suffix]









    @property
    def chords(self):
        return self._parsed.chords

    @property
    def events(self):
        return self._parsed.events

    @property
    def expanded(self):
        if self._annotations is None:
            return None
        return self._annotations.expanded

    @property
    def labels(self):
        if self._annotations is None:
            return None
        return self._annotations.get_labels(**self.labels_cfg)

    @property
    def measures(self):
        return self._parsed.ml

    @property
    def notes(self):
        return self._parsed.nl

    @property
    def notes_and_rests(self):
        return self._parsed.notes_and_rests

    @property
    def parsed(self):
        if self._parsed is None:
            self.logger.error("Score has not been parsed yet.")
            return None
        return self._parsed

    @property
    def rests(self):
        return self._parsed.rl

    @property
    def staff_ids(self):
        return self._parsed.staff_ids


    @property
    def version(self):
        """MuseScore version with which the file was created (read-only)."""
        return self._parsed.version


    # def __getstate__(self):
    #     self.logger.logger.handlers = []
    #     return self.__dict__