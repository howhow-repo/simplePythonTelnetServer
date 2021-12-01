class IndataHandler:

    @staticmethod
    def echo(indata: bin) -> str:
        indata = indata.decode()
        resp = f"echo: {indata}"
        return resp
