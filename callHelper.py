"""
getters and setters
"""
class NestedDictionary(object):


    def __init__(self,
                 *args,
                 **kwargs):
        self.dict = dict(*args, **kwargs)


    def __getitem__(self,
                    keys):
    
        if not isinstance(keys, tuple):
            if isinstance(keys, str) or isinstance(keys, int):
                keys = (keys, )
            else:
                keys = tuple(keys)


        branch_ = self.dict

        for key in keys:branch_ = branch_[key]

        return NestedDictionary(branch_).dict if isinstance(branch_, dict) else branch_


    def __setitem__(self,
                    keys,
                    value):
        if not isinstance(keys, tuple):
            if len(keys) < 2: keys = (*keys, )
            else: keys = tuple(keys)
        
        branch_ = self.dict

        for key in keys[:-1]:
            if not key in branch_:
                branch_[key] = {}
            branch_ = branch_[key]

        branch_[keys[-1]] = value


    def __keys__(self,
                 depth = 0):
        keys = [[k] for k in self.dict.keys()]
        for k in keys:
            branch_ = self[k[0]]
            self.__recurse_keys__(key = k[0], 
                                  branch = branch_, 
                                  keyList = k)
            branch_ = self[k[0]]
            if isinstance(branch_, dict):
                if len(branch_.keys()) > 1:
                    b_keys = list(branch_.keys())
                    length = len(b_keys)
                    # Copies of k to append the keys in the last layer to. When multiple keys are in the last layer,
                    # we need new trees to capture all key paths
                    new_trees = [k for _ in range(length)]
                    k.append(b_keys[0])  # Add the first key to the original tree
                    for i in range(1, length):
                        tree = new_trees[i]
                        tree.append(b_keys[i])
                        keys.append(tree)
                else:
                    k.append(list(branch_.keys())[0])
            while not isinstance(branch_, dict):
                branchKeys = [[bk] for bk in branch_.dict.keys()]

        return keys




    def __recurse_keys__(branch,
                         keyList,
                         depth = 0):

        bolKeys = list(branch.keys())
    
        if isinstance(bolKeys, dict):
            if len(bolKeys) > 1:
                length_ = len(bolKeys)

                newTrees = [keyList for _ in range(1, length_)]
                keyList.append(bolKeys[0])

                combinedKlists = [keyList]

                for k_ in range(length_ - 1):
                    tree_ = newTrees[k_]
                    tree_.append(bolKeys[k_])
                    combinedKlists.append(tree_)
                return combinedKlists
            else: return keyList.append(list(branch.keys())[0])
        else:pass






































