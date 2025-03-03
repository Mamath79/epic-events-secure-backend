from crm.services.company_service import CompanyService
from crm.database.base import SessionLocal
from rich.console import Console

console = Console()

def get_companies_list():
    """Récupère et affiche la liste des entreprises existantes."""
    session = SessionLocal()
    company_service = CompanyService(session)
    companies = company_service.get_all()
    session.close()
    
    return companies

def create_company():
    """Demande le nom d'une nouvelle entreprise et la crée."""
    new_company_title = console.input("[bold cyan]Nom de la nouvelle entreprise : [/bold cyan]").strip()
    new_company_siret = console.input("[bold cyan]Siret de l'entreprise : [/bold cyan]").strip()
    
    if not new_company_title:
        console.print("[red]❌ Le nom de l'entreprise est requis.[/red]")
        return None

    session = SessionLocal()
    company_service = CompanyService(session)
    
    new_company = company_service.create({"title": new_company_title, "siret": new_company_siret})
    session.close()

    console.print(f"✅ [green]Entreprise '{new_company.title}' ajoutée avec succès ![/green]")
    return new_company
