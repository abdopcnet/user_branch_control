import frappe


def validate_branch_write_access(doc, method=None):
    """
    Validate user has write access to the branch
    Prevents users from writing to branches they're restricted from
    """
    if doc.branch:
        user = frappe.session.user
        
        if user != "Administrator":
            user_branch_record = frappe.get_all(
                "user_branch_control",
                filters={
                    "user": user,
                    "branch": doc.branch,
                    "disable_write": 1
                },
                limit=1
            )
            
            if user_branch_record:
                frappe.throw(
                    f"ليس لديك صلاحية الكتابة في الفرع: {doc.branch}",
                    title="صلاحية مقيدة"
                )
