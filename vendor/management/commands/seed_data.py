from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Vendor.objects.all().delete()
        Product.objects.all().delete()
        Course.objects.all().delete()
        Certification.objects.all().delete()
        VendorProductMapping.objects.all().delete()
        ProductCourseMapping.objects.all().delete()
        CourseCertificationMapping.objects.all().delete()

        # Create Vendors
        self.stdout.write('Creating vendors...')
        vendors = [
            Vendor.objects.create(
                name='TechCorp International',
                code='TECH001',
                description='Leading technology and software solutions provider',
                is_active=True
            ),
            Vendor.objects.create(
                name='Acme Learning Systems',
                code='ACME001',
                description='Educational technology solutions',
                is_active=True
            ),
            Vendor.objects.create(
                name='Global Tech Training',
                code='GTT001',
                description='Professional training and development',
                is_active=True
            ),
        ]

        # Create Products
        self.stdout.write('Creating products...')
        products = [
            Product.objects.create(
                name='Java Development Platform',
                code='JAVA001',
                description='Comprehensive Java development ecosystem',
                is_active=True
            ),
            Product.objects.create(
                name='Python Data Science Suite',
                code='PY001',
                description='Python tools for data science and ML',
                is_active=True
            ),
            Product.objects.create(
                name='Web Development Framework',
                code='WEB001',
                description='Modern web development with Django and React',
                is_active=True
            ),
            Product.objects.create(
                name='Cloud Infrastructure Platform',
                code='CLOUD001',
                description='Cloud-native application deployment',
                is_active=True
            ),
        ]

        # Create Courses
        self.stdout.write('Creating courses...')
        courses = [
            Course.objects.create(
                name='Java Fundamentals',
                code='JAVA101',
                description='Learn Java programming from basics to advanced',
                is_active=True
            ),
            Course.objects.create(
                name='Advanced Java Development',
                code='JAVA201',
                description='Expert-level Java development patterns',
                is_active=True
            ),
            Course.objects.create(
                name='Python for Data Science',
                code='PY101',
                description='Master Python for data analysis and visualization',
                is_active=True
            ),
            Course.objects.create(
                name='Django Web Development',
                code='WEB101',
                description='Full-stack web development with Django',
                is_active=True
            ),
            Course.objects.create(
                name='Cloud Architecture Essentials',
                code='CLOUD101',
                description='Design and deploy cloud applications',
                is_active=True
            ),
        ]

        # Create Certifications
        self.stdout.write('Creating certifications...')
        certifications = [
            Certification.objects.create(
                name='Oracle Java Associate',
                code='OJA001',
                description='Official Oracle Java certification',
                is_active=True
            ),
            Certification.objects.create(
                name='AWS Solutions Architect',
                code='AWS001',
                description='Amazon Web Services certification',
                is_active=True
            ),
            Certification.objects.create(
                name='Python Developer Certificate',
                code='PYC001',
                description='Professional Python developer certification',
                is_active=True
            ),
            Certification.objects.create(
                name='Django Web Developer',
                code='DJG001',
                description='Certified Django web developer',
                is_active=True
            ),
        ]

        # Create Vendor-Product Mappings
        self.stdout.write('Creating vendor-product mappings...')
        VendorProductMapping.objects.create(
            vendor=vendors[0],
            product=products[0],
            primary_mapping=True,
            is_active=True
        )
        VendorProductMapping.objects.create(
            vendor=vendors[0],
            product=products[1],
            primary_mapping=False,
            is_active=True
        )
        VendorProductMapping.objects.create(
            vendor=vendors[1],
            product=products[2],
            primary_mapping=True,
            is_active=True
        )
        VendorProductMapping.objects.create(
            vendor=vendors[2],
            product=products[3],
            primary_mapping=True,
            is_active=True
        )

        # Create Product-Course Mappings
        self.stdout.write('Creating product-course mappings...')
        ProductCourseMapping.objects.create(
            product=products[0],
            course=courses[0],
            primary_mapping=True,
            is_active=True
        )
        ProductCourseMapping.objects.create(
            product=products[0],
            course=courses[1],
            primary_mapping=False,
            is_active=True
        )
        ProductCourseMapping.objects.create(
            product=products[1],
            course=courses[2],
            primary_mapping=True,
            is_active=True
        )
        ProductCourseMapping.objects.create(
            product=products[2],
            course=courses[3],
            primary_mapping=True,
            is_active=True
        )
        ProductCourseMapping.objects.create(
            product=products[3],
            course=courses[4],
            primary_mapping=True,
            is_active=True
        )

        # Create Course-Certification Mappings
        self.stdout.write('Creating course-certification mappings...')
        CourseCertificationMapping.objects.create(
            course=courses[0],
            certification=certifications[0],
            primary_mapping=True,
            is_active=True
        )
        CourseCertificationMapping.objects.create(
            course=courses[1],
            certification=certifications[0],
            primary_mapping=False,
            is_active=True
        )
        CourseCertificationMapping.objects.create(
            course=courses[2],
            certification=certifications[2],
            primary_mapping=True,
            is_active=True
        )
        CourseCertificationMapping.objects.create(
            course=courses[3],
            certification=certifications[3],
            primary_mapping=True,
            is_active=True
        )
        CourseCertificationMapping.objects.create(
            course=courses[4],
            certification=certifications[1],
            primary_mapping=True,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with sample data!'))
        self.stdout.write(f'Created {len(vendors)} vendors')
        self.stdout.write(f'Created {len(products)} products')
        self.stdout.write(f'Created {len(courses)} courses')
        self.stdout.write(f'Created {len(certifications)} certifications')
