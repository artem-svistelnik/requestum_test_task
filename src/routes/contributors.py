from typing import Annotated

from fastapi import APIRouter, Request, Form
from app.core.config import templates
import requests
from app.core.config import settings


contributors_router = APIRouter(prefix="/contributors", tags=["Contributors"])


async def get_response(url):
    headers = {
        "Authorization": "Bearer " + settings.GITGUB_PERSONAL_TOKEN,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    return None


async def get_contributors_repos(repo_url):
    if str(repo_url).endswith("/"):
        repo_url = repo_url[0:-1]

    splitted_repo_url = repo_url.split("/")
    repo_owner = splitted_repo_url[-2]
    repo_name = splitted_repo_url[-1]
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"
    response = await get_response(url)
    if response is not None:
        contributors = response.json()
        repos_url = [contributor.get("repos_url") for contributor in contributors]
        contributor_names = [contributor.get("login") for contributor in contributors]
        return repos_url, contributor_names
    return [], []


async def get_contributors(full_name):
    url = f"https://api.github.com/repos/{full_name}/contributors"
    response = await get_response(url)
    if response is not None:
        contributors = response.json()
        return contributors
    return {}


async def get_repo_contributors(repos_list_url):
    response = await get_response(repos_list_url)
    repos = response.json()
    repo_contributors = {}
    for repo in repos:
        contributors = await get_contributors(repo.get("full_name"))
        logins = [contributor.get("login") for contributor in contributors]
        repo_contributors[repo.get("full_name")] = logins
    return repo_contributors


def get_top_repositories(repo_contributors, contributor_names):
    contributors_count = {}

    for repo, contributors in repo_contributors.items():
        count = sum(
            1 for contributors in contributors if contributors in contributor_names
        )
        contributors_count[repo] = {
            "count": count,
            "contributors": contributors,
            "repo": repo,
        }

    sorted_repositories = sorted(
        contributors_count.items(), key=lambda x: x[1]["count"], reverse=True
    )
    top_5 = [
        {
            "repository": repo,
            "count": data["count"],
        }
        for repo, data in sorted_repositories[:5]
    ]
    return top_5


@contributors_router.get("")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@contributors_router.post("")
async def get_top_project(request: Request, repo_url: Annotated[str, Form()]):
    contributors_repos_url, contributor_names = await get_contributors_repos(repo_url)
    repo_contributors = {}
    for url in contributors_repos_url:
        repo_contributors.update(await get_repo_contributors(url))
    top_repo = get_top_repositories(repo_contributors, contributor_names)

    return templates.TemplateResponse(
        "home.html", {"request": request, "top_repo": top_repo}
    )
