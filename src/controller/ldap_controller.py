import re
from typing import Any

from src.component.ldap import LDAPServer
from src.config import config


class LDAPController:
    def __init__(self) -> None:
        self.ldap_server = LDAPServer(host=config.ldap_server, user=config.ldap_user, password=config.ldap_password)
        self.attributes: dict = {
            "cn": "姓名",
            "st": "位置",
            "distinguishedName": "部門",
            "mail": "信箱",
            "mobile": "手機",
            "telephoneNumber": "分機號碼",
        }
        self.split_line: str = f"{'-'*40}\n"

    def extract_department(self, input_string: str):
        pattern = r"OU=([^,]+)"

        matches = re.findall(pattern, input_string)

        extracted_info = ",".join(matches)

        return extracted_info

    def get_split_line_length(self):
        return len(self.split_line)

    def append_split_line(self, text_string: str):
        text_string += self.split_line
        return text_string

    def serialize_to_split_list(self, entries: list[Any], max_length: int):
        split_line_length = self.get_split_line_length()
        m_length = max_length - 2 * split_line_length
        l = len(entries)
        result_list = []
        result = ""
        result = self.append_split_line(result)  # start
        curr_length = 0
        curr_length += split_line_length

        while entries:
            entry = entries.pop()
            t_str = ""
            for k, v in self.attributes.items():
                if v == "部門":
                    t_str += f"**{v}**: {self.extract_department(getattr(entry, k).value) or '無資料'}\n"
                else:
                    t_str += f"**{v}**: {getattr(entry, k).value or '無資料'}\n"
            t_length = len(t_str)
            if curr_length + t_length < m_length:
                result += t_str
                result = self.append_split_line(result)
                curr_length += t_length
                curr_length += split_line_length
            else:
                result_list.append(result)
                result = ""
                result = self.append_split_line(result)  # start
                curr_length = 0
                curr_length += split_line_length

        if l == 0:
            result = "找不到聯絡人。\n"
        result_list.append(result)
        return result_list

    def serialize_autocomplete(self, entries: list):
        return [
            {
                "name": getattr(entry, "cn").value,
                "value": getattr(entry, "cn").value,
            }
            for entry in entries
        ]

    async def get_all_names(self):
        entries = self.ldap_server.search(
            "dc=actgenomics,dc=com",
            "(&(objectCategory=person)(objectClass=organizationalPerson))",
            attributes=["cn"],
        )
        return [entry["cn"].value for entry in entries]

    def autocomplete_search(self, search_string: str):
        search_string = search_string.replace("(", "\\28").replace(")", "\\29")
        entries = self.ldap_server.search(
            "dc=actgenomics,dc=com",
            f"(&(objectCategory=person)(objectClass=organizationalPerson)(cn=*{search_string}*))",
            attributes=["cn"],
        )
        return self.serialize_autocomplete(entries)

    async def search(self, search_string: str, max_length: int):
        search_string = search_string.replace("(", "\\28").replace(")", "\\29")
        entries = self.ldap_server.search(
            "dc=actgenomics,dc=com",
            f"(&(objectCategory=person)(objectClass=organizationalPerson)(cn=*{search_string}*))",
            attributes=self.attributes.keys(),
        )
        return self.serialize_to_split_list(entries, max_length)


if __name__ == "__main__":
    import asyncio
    async def main():
        ldap_controller = LDAPController()
        r = await ldap_controller.search("Jian Siao Yu (簡孝羽)", 2000)
        print("do next job")
        print(r)

    asyncio.run(main())
