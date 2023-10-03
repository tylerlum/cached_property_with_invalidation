def cached_property_with_invalidation(invalidation_variable_name: str):
    """Decorator to create cached_property that can be invalidated when invalidation variable is updated

    Args:
        invalidation_variable_name (str): instance variable name that will be used to invalidate the cached_property if updated to new value
    """

    def decorator(property_method):
        @property
        def wrapped_method(self):
            property_name = property_method.__name__
            VERBOSE = False

            assert hasattr(
                self, invalidation_variable_name
            ), f"Instance variable {invalidation_variable_name} does not exist"
            invalidation_variable = getattr(self, invalidation_variable_name)

            # Dict of dicts to store cache
            # First key: invalidation variable
            # Second key: property name
            cache_dict_name = "_property_with_invalidation_dict"
            if not hasattr(self, cache_dict_name):
                setattr(self, cache_dict_name, {})
            cache_dict = getattr(self, cache_dict_name)

            if invalidation_variable not in cache_dict:
                cache_dict[invalidation_variable] = {}

            if not property_name in cache_dict[invalidation_variable]:
                if VERBOSE:
                    print(f"Recomputing for {property_name}")
                new_value = property_method(self)
                # Update cache
                cache_dict[invalidation_variable][property_name] = new_value
                return new_value
            else:
                if VERBOSE:
                    print(f"Using cache for {property_name}")
                return cache_dict[invalidation_variable][property_name]

        return wrapped_method

    return decorator
