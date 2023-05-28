from docker import run_cmd


class Honeypot:
    def __init__(self, name: str, image_name: str, password: str) -> None:
        self.name = name
        self.container_name = f"auto-{self.name}"
        self.image_name = image_name
        self.password = password
        self.start_cmd = f"docker run -d --name {self.container_name} --hostname {self.container_name} {self.image_name}"
        self.logs_cmd = f"docker logs {self.container_name}"
        self.stop_cmd = (
            f"docker stop {self.container_name} && docker rm {self.container_name}"
        )

    def start(self):
        return run_cmd(self.start_cmd)

    def logs(self):
        return run_cmd(self.logs_cmd)

    def stop(self):
        return run_cmd(self.stop_cmd)


HONEYPOTS = {
    "kippo": Honeypot(
        name="kippo",
        image_name="tomdesinto/kippo",
        password="123456",
    ),
    "cowrie": Honeypot(name="cowrie", image_name="cowrie/cowrie:latest", password=""),
}
