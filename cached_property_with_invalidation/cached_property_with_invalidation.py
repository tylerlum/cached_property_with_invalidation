def cached_property_with_invalidation(
    invaidation_variable_name: str, cached_property_name: str
):
    """Decorator to create cached_property that can be invalidated when invalidation variable is updated

    Args:
        invaidation_variable_name (str): instance variable name that will be used to invalidate the cached_property if updated to new value
        cached_property_name (str): Name
    """

    def decorator(cached_property_method):
        def wrapped_cached_property_method(self):
            VERBOSE = False

            assert hasattr(
                self, invaidation_variable_name
            ), f"Instance variable {invaidation_variable_name} does not exist"
            invalidation_variable = getattr(self, invaidation_variable_name)

            # Custom variable names to store
            cached_invalidation_variable_name = (
                f"_cached_invalidation_variable_for_{cached_property_name}"
            )
            cached_value_variable_name = f"_cached_value_for_{cached_property_name}"

            # Return cached value
            if hasattr(
                self, cached_invalidation_variable_name
            ) and invalidation_variable == getattr(
                self, cached_invalidation_variable_name
            ):
                if VERBOSE:
                    print(f"USING CACHE for {cached_property_name}")
                return getattr(self, cached_value_variable_name)

            # Update cached value
            if VERBOSE:
                print(f"UPDATING CACHE for {cached_property_name}")
            new_value = cached_property_method(self)
            setattr(self, cached_value_variable_name, new_value)
            setattr(self, cached_invalidation_variable_name, invalidation_variable)
            return new_value
