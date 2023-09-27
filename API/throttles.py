from rest_framework import throttling


class TenCallsPerMinute(throttling.UserRateThrottle):
    scope = 'ten'
