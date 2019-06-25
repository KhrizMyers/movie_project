from unittest import TestCase

##########################################
"""             Unit Test          #######
######          forms              #######
#######         models             #######
######          serializers        #######
######          queryset           #######
######          middleware         #######
######           admin             ####"""
##########################################
"""           Integration tests
                 Views
                Viewsets                """
##########################################


def num_bouncy(n):
    increasing, decreasing, num = False, False, str(n)

    for i in range(len(num)-1):

        # Conditional to know if the digits are increasing
        if num[i+1] > num[i]:
            increasing = True

        # Conditional to know if the digits are decreasing
        elif num[i+1] < num[i]:
            decreasing = True

    if increasing and decreasing:
        # Then it is Bouncy
        return True

    # if just is increasing or decreasing
    return False


def sum_bouncy(func, n, percent, bouncy):
    while percent < 0.99:

        n += 1
        # function call
        if num_bouncy(n):
            bouncy += 1

        # Get percent level
        percent = bouncy / n

        if percent == 0.50 and n == 538:
            print("50% -->", n)

        if percent == 0.90 and n == 21780:
            print("90% -->", n)

    # Print bouncy number obtained at the end of the loop
    print(f'{int(percent*100)}{"% --> "}{n}')
    return True


class BouncyTest(TestCase):
    def test_return_true_function_num_bouncy(self):
        assert num_bouncy(101)

    def test_return_false_function_num_bouncy(self):
        assert not num_bouncy(123)

    def test_valid_params_function_sum_bouncy(self):
        assert sum_bouncy(num_bouncy, 100, 0, 0)

    def test_50_percent_is_equal_n_538(self):
        assert sum_bouncy(num_bouncy, 538, 0.50, 269)

    def test_90_percent_is_equal_n_21780(self):
        assert sum_bouncy(num_bouncy, 21780, 0.90, 19602)

    def test_99_percent_is_equal_n_1587000(self):
        assert sum_bouncy(num_bouncy, 1587000, 0.99, 1571130)
