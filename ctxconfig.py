import pandas as pd


class Context:
    def __init__(self, env='', app='', user='', machine=''):
        self.env = env
        self.app = app
        self.user = user
        self.machine = machine

    def __repr__(self) -> str:
        return str(vars(self))


class Config:
    def __init__(self, config_file):
        self._df = pd.read_csv(config_file, keep_default_na=False)
        self._df.set_index('key', inplace=True)
        print(self._df.to_string())

    def get_value(self, key, context=None):
        c = context or Context()
        if key not in self._df.index:
            raise KeyError(f'No config found for key = {key}, context = {context}')
        try:
            df: pd.DataFrame = self._df.loc[[key]]  # https://stackoverflow.com/a/20384317
        except:
            raise Exception(f'Error while finding config for key = {key}, context = {context}')

        def check(hits):
            if len(hits) == 1:
                return hits['value'].values[0]

        return check(df.loc[(df['env'] == c.env) & (df['app'] == c.app) & (df['user'] == c.user) & (df['machine'] == c.machine)]) or \
               check(df.loc[(df['env'] == c.env) & (df['app'] == c.app) & (df['machine'] == c.machine)]) or \
               check(df.loc[(df['env'] == c.env) & (df['app'] == c.app) & (df['user'] == c.user)]) or \
               check(df.loc[(df['env'] == c.env) & (df['machine'] == c.machine)]) or \
               check(df.loc[(df['env'] == c.env) & (df['user'] == c.user)]) or \
               check(df.loc[(df['env'] == c.env) & (df['app'] == c.app)]) or \
               check(df.loc[(df['env'] == c.env)]) or \
               check(df)

    def get_int_value(self, key, context):
        return int(self.get_value(key, context))

    def get_float_value(self, key, context):
        return float(self.get_value(key, context))

    def get_bool_value(self, key, context):
        value = self.get_value(key, context)
        return str(value).lower() in ("yes", "true", "t", "1")


def main():
    config = Config('config_data.csv')
    keys = ['key1', 'key2', 'key3']
    contexts = [
        None,
        Context(),
        Context('dev'),
        Context('dev', 'app1'),
        Context('dev', user='user1'),
        Context('dev', 'app1', 'user1'),
        Context('dev', 'app1', machine='machine1'),
        Context('dev', 'app1', 'user1', 'machine1'),
        Context('prod'),
        Context('prod', 'app1'),
        Context('prod', user='user1'),
        Context('prod', 'app1', 'user1'),
        Context('prod', 'app1', machine='machine1'),
        Context('prod', 'app1', 'user1', 'machine1')
    ]

    def check_config(func, key, context=None):
        value = func(key, context)
        print(f'{key} = {value} for context: {context}')

    for key in keys:
        for context in contexts:
            check_config(config.get_value, key, context)

    check_config(config.get_int_value, 'key_for_int')
    check_config(config.get_float_value, 'key_for_float')
    check_config(config.get_bool_value, 'key_for_bool_true')
    check_config(config.get_bool_value, 'key_for_bool_yes')
    check_config(config.get_bool_value, 'key_for_bool_t')
    check_config(config.get_bool_value, 'key_for_bool_1')
    check_config(config.get_bool_value, 'key_for_bool_false')
    check_config(config.get_bool_value, 'key_for_bool_no')
    check_config(config.get_bool_value, 'key_for_bool_f')
    check_config(config.get_bool_value, 'key_for_bool_0')


if __name__ == '__main__':
    main()

