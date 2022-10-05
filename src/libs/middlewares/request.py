def RequestMiddleware(get_response):

    def middleware(request):
        print(request)
        response = get_response(request)
        print(
            request.META.get("REMOTE_ADDR"),
            request.method,
            request.path,
            response.status_code
        )

        return response

    return middleware
