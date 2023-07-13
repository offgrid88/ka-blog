db.createUser(
  {
    user: "mdx8",
    pwd:  passwordPrompt(),
    roles: [ { role: "readWrite", db: "offgrid8" } ]
  }
)

created_at
author


db.grantRolesToUser(
    "mdx8",
    [ "readWrite" , { role: "dbOwner", db: "offgrid8_db" } ],
 )