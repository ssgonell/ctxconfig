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

    def get_value(self, key, context):
        c = context
        df = self._df.loc[key]
        result = df.loc[(df['env'] == c.env) & (df['app'] == c.app) & (df['user'] == c.user) & (df['machine'] == c.machine)]
        if len(result) == 1:
            return result['value'].values[0]
        result = df.loc[(df['env'] == c.env) & (df['app'] == c.app) & (df['user'] == c.user)]
        if len(result) == 1:
            return result['value'].values[0]
        result = df.loc[(df['env'] == c.env) & (df['app'] == c.app)]
        if len(result) == 1:
            return result['value'].values[0]
        result = df.loc[(df['env'] == c.env)]
        if len(result) == 1:
            return result['value'].values[0]
        result = df
        if len(result) == 1:
            return result['value'].values[0]


def check_config(config, key, context):
    value = config.get_value(key, context)
    print(f'{key} = {value} for context: {context}')


def main():
    config = Config('config_data.csv')
    keys = ['key1', 'key2', 'key3']
    contexts = [
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
    for key in keys:
        for context in contexts:
            check_config(config, key, context)


if __name__ == '__main__':
    main()

