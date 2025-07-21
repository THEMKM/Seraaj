"""Reporting utilities for Seraaj analytics prototype."""

import csv
from datetime import datetime
from typing import Dict, Iterable

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import VolunteerEvent


def generate_organization_report(
    org_id: str, events: Iterable[VolunteerEvent]
) -> Dict[str, float]:
    """Aggregate volunteer hours and opportunity completion count for an organization."""
    total_hours = 0.0
    opportunities = set()
    volunteers = set()
    for ev in events:
        if ev.organization_id != org_id:
            continue
        total_hours += ev.hours
        opportunities.add(ev.opportunity_id)
        volunteers.add(ev.volunteer_id)
    return {
        "total_hours": total_hours,
        "opportunities_completed": len(opportunities),
        "unique_volunteers": len(volunteers),
    }


def export_organization_report_csv(
    org_id: str, events: Iterable[VolunteerEvent], output_path: str
) -> None:
    """Export an organization's report to a CSV file."""
    report = generate_organization_report(org_id, events)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for key, value in report.items():
            writer.writerow([key, value])


def generate_volunteer_certificate(
    volunteer_id: str, events: Iterable[VolunteerEvent], output_path: str
) -> None:
    """Generate a simple PDF certificate summarizing volunteer hours."""
    total_hours = sum(ev.hours for ev in events if ev.volunteer_id == volunteer_id)
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(300, 700, "Certificate of Volunteering")
    c.setFont("Helvetica", 12)
    c.drawCentredString(300, 650, f"Presented to {volunteer_id}")
    c.drawCentredString(300, 630, f"Total Hours Contributed: {total_hours:.1f}")
    c.drawCentredString(300, 610, f"Date: {datetime.utcnow().date().isoformat()}")
    c.showPage()
    c.save()


def platform_overview(events: Iterable[VolunteerEvent]) -> Dict[str, int]:
    """Return basic counts of volunteers, organizations and opportunities."""
    volunteers = set()
    organizations = set()
    opportunities = set()
    for ev in events:
        volunteers.add(ev.volunteer_id)
        organizations.add(ev.organization_id)
        opportunities.add(ev.opportunity_id)
    return {
        "total_volunteers": len(volunteers),
        "total_organizations": len(organizations),
        "total_opportunities": len(opportunities),
    }
